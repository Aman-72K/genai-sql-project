# GenAI SQL Analyst

A powerful AI-powered SQL query assistant that converts natural language questions into SQL queries and provides actionable insights. Built with Agno, Gradio, and OpenRouter.

## 🚀 Features

- **Natural Language to SQL**: Convert plain English questions into optimized SQL queries
- **Multi-Database Support**: Connect to SQLite, PostgreSQL, MySQL, and other SQLAlchemy-supported databases
- **Structured Responses**: Get SQL queries, execution results, and actionable insights in a clear format
- **Web Interface**: User-friendly Gradio web app for easy interaction
- **Sample Database**: Includes a sample cafe business database for testing
- **Comprehensive Testing**: Full test suite with unit tests for all components

## 📋 Prerequisites

- Python 3.8+
- OpenRouter API key (for AI model access)
- SQLite/PostgreSQL/MySQL database (or any SQLAlchemy-compatible database)

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/f20221229-cloud/genai-sql-project.git
   cd genai-sql-project
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env.local` file in the project root:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

## 🗄️ Database Setup

### Option 1: Use the Sample Database
Run the setup script to create a sample cafe business database:
```bash
python setup_db.py
```
This creates `cafe_business.db` with three tables:
- `coffee_products`: Product catalog with prices
- `inventory_status`: Stock levels and reorder points
- `daily_sales`: Transaction records

### Option 2: Connect to Your Own Database
The app supports any SQLAlchemy-compatible database URL format:
- SQLite: `sqlite:///path/to/database.db`
- PostgreSQL: `postgresql://user:password@localhost:5432/dbname`
- MySQL: `mysql+pymysql://user:password@localhost:3306/dbname`

## 🚀 Usage

1. **Start the application:**
   ```bash
   python app.py
   ```

2. **Open your browser** to the URL shown (typically http://localhost:7860)

3. **Connect to a database:**
   - Enter your database URL in the text field
   - Click "Connect"
   - Examples:
     - `sqlite:///cafe_business.db` (for the sample database)
     - `postgresql://user:pass@localhost:5432/mydb`

4. **Ask questions in natural language:**
   - "What are the top-selling products?"
   - "Show me products with low inventory"
   - "What's the total revenue by category?"

The AI agent will:
1. **Analyze** your database schema
2. **Generate** optimized SQL queries
3. **Execute** the queries
4. **Return** structured responses with:
   - The SQL query used
   - Query results in a formatted table
   - 2-3 actionable insights with specific data points

## 🧪 Testing

Run the test suite to ensure everything works correctly:
```bash
python -m pytest tests/
```

Or run individual test files:
```bash
python -m pytest tests/test_agent.py
python -m pytest tests/test_app.py
python -m pytest tests/test_csv_handler.py
```

## 📁 Project Structure

```
GenAI_SQL/
├── agent.py              # AI agent configuration with Agno
├── app.py                # Gradio web interface
├── csv_handler.py        # Legacy CSV handling (deprecated)
├── setup_db.py          # Sample database creation script
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── tests/
    ├── test_agent.py    # Agent functionality tests
    ├── test_app.py      # Web app tests
    └── test_csv_handler.py  # CSV handler tests
```

## 🔧 Configuration

### AI Model
The app uses the `minimax/minimax-m2.7` model via OpenRouter. To change models, modify the `model` parameter in `agent.py`:

```python
model=OpenRouter(id="your-preferred-model")
```

### Response Format
The agent is configured to provide structured responses with:
1. **SQL Query**: The generated SQL in a code block
2. **Tool Result**: Formatted query results
3. **Final Insights**: 2-3 actionable insights

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run the test suite: `python -m pytest tests/`
5. Commit your changes: `git commit -am 'Add new feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Agno](https://github.com/agno-agi/agno) - The AI agent framework
- [Gradio](https://gradio.app/) - Web interface library
- [OpenRouter](https://openrouter.ai/) - AI model API access
- [SQLAlchemy](https://sqlalchemy.org/) - Database toolkit

## 🆘 Troubleshooting

### Connection Issues
- **SQLite**: Use absolute paths or place the database file in the project directory
- **PostgreSQL/MySQL**: Ensure the database server is running and credentials are correct

### API Key Issues
- Verify your OpenRouter API key is valid and has sufficient credits
- Check that `.env.local` is in the project root directory

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Try recreating the virtual environment if issues persist

For more help, check the test files or open an issue on GitHub.