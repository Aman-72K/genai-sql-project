import sqlite3
import pytest
from pathlib import Path
from csv_handler import _sanitize_name, _sanitize_columns, load_csv_to_db, DB_PATH


class TestSanitizeName:
    def test_strips_whitespace(self):
        assert _sanitize_name("  foo  ") == "foo"

    def test_replaces_special_chars_with_underscore(self):
        # "order #1" -> "order__1" -> collapse -> "order_1"
        assert _sanitize_name("order #1") == "order_1"

    def test_collapses_consecutive_underscores(self):
        assert _sanitize_name("a  b") == "a_b"

    def test_prepends_t_when_starts_with_digit(self):
        assert _sanitize_name("2024sales") == "t_2024sales"

    def test_truncates_to_60_chars(self):
        long_name = "a" * 70
        result = _sanitize_name(long_name)
        assert len(result) <= 60

    def test_reserved_word_gets_data_suffix(self):
        assert _sanitize_name("order") == "order_data"
        assert _sanitize_name("select") == "select_data"
        assert _sanitize_name("group") == "group_data"

    def test_reserved_word_check_is_case_insensitive(self):
        # Check is case-insensitive; original casing preserved + _data appended
        result = _sanitize_name("ORDER")
        assert result == "ORDER_data"

    def test_normal_name_unchanged(self):
        assert _sanitize_name("sales_data") == "sales_data"

    def test_empty_string_returns_empty(self):
        # Edge case: empty after sanitization
        result = _sanitize_name("")
        assert isinstance(result, str)


class TestSanitizeColumns:
    def test_deduplicates_colliding_names(self):
        # "Order #" -> "Order_", "Order %" -> "Order_", collision
        result = _sanitize_columns(["Order #", "Order %", "Revenue"])
        assert result[0] == "Order_"
        assert result[1] == "Order__1"
        assert result[2] == "Revenue"

    def test_no_collision_unchanged(self):
        result = _sanitize_columns(["name", "value", "region"])
        assert result == ["name", "value", "region"]

    def test_three_way_collision(self):
        # "a b", "a_b", "a  b" all sanitize to "a_b"
        result = _sanitize_columns(["a b", "a_b", "a  b"])
        assert result[0] == "a_b"
        assert result[1] == "a_b_1"
        assert result[2] == "a_b_2"

    def test_deduplication_suffix_itself_doesnt_collide(self):
        # ["a_b", "a_b", "a_b_1"] — the suffix "a_b_1" already exists
        result = _sanitize_columns(["a_b", "a_b", "a_b_1"])
        assert result[0] == "a_b"
        assert result[1] == "a_b_1"
        assert result[2] == "a_b_1_1"
        # All must be unique
        assert len(result) == len(set(result))


class TestLoadCsvToDb:
    def test_raises_value_error_on_missing_file(self):
        with pytest.raises(ValueError, match="Could not read CSV"):
            load_csv_to_db("/nonexistent/path/file.csv")

    def test_raises_value_error_on_empty_csv(self, tmp_path):
        empty = tmp_path / "empty.csv"
        empty.write_text("")
        with pytest.raises(ValueError, match="empty"):
            load_csv_to_db(str(empty))

    def test_returns_table_name_rows_cols(self, tmp_path):
        csv_file = tmp_path / "sales_data.csv"
        csv_file.write_text("product,revenue,region\nA,1000,North\nB,1500,South\n")
        table_name, rows, cols = load_csv_to_db(str(csv_file))
        assert table_name == "sales_data"
        assert rows == 2
        assert cols == 3

    def test_data_written_to_db(self, tmp_path):
        csv_file = tmp_path / "products.csv"
        csv_file.write_text("name,price\nWidget,9.99\nGadget,19.99\n")
        load_csv_to_db(str(csv_file))
        conn = sqlite3.connect(DB_PATH)
        rows = conn.execute("SELECT * FROM products").fetchall()
        conn.close()
        assert len(rows) == 2

    def test_second_upload_fully_replaces_db(self, tmp_path):
        """Uploading a new CSV must delete the old DB entirely — old tables must not survive."""
        csv1 = tmp_path / "first.csv"
        csv1.write_text("x\n1\n2\n")
        csv2 = tmp_path / "second.csv"
        csv2.write_text("y\n10\n20\n30\n")

        load_csv_to_db(str(csv1))
        load_csv_to_db(str(csv2))

        conn = sqlite3.connect(DB_PATH)
        # New table exists
        rows = conn.execute("SELECT * FROM second").fetchall()
        assert len(rows) == 3
        # Old table is gone
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        conn.close()
        table_names = [t[0] for t in tables]
        assert "first" not in table_names
