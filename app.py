import os
import traceback

import gradio as gr
from dotenv import load_dotenv

from agent import get_agent

load_dotenv(".env.local")

# Module-level agent state. Safe for one-user-at-a-time deployment.
# demo.queue(max_size=1) serializes events to prevent concurrent mutation.
current_agent = None  # agno Agent | None
current_db_url = None  # str | None


def connect_db_handler(db_url):
    """
    Handle database URL input: create agent, clear chat.
    Returns (status, chatbot, send_button, msg_textbox) component updates.
    """
    global current_agent, current_db_url

    if not db_url or not db_url.strip():
        current_agent = None
        current_db_url = None
        return (
            gr.update(value="❌ No database URL provided. Enter a valid connection string."),
            [],
            gr.update(interactive=False),
            gr.update(interactive=False),
        )

    db_url = db_url.strip()
    

    try:
        print(f"Attempting to connect to database: {db_url}")
        new_agent = get_agent(db_url)
        current_agent = new_agent
        current_db_url = db_url
        return (
            gr.update(value=f"✅ Connected to database: `{db_url}`"),
            [],
            gr.update(interactive=True),
            gr.update(interactive=True),
        )
    except Exception as e:
        print(f"Connection error: {type(e).__name__}: {e}")
        print("Full traceback:")
        print(traceback.format_exc())
        current_agent = None
        current_db_url = None
        return (
            gr.update(value=f"❌ Connection error: {e}"),
            [],
            gr.update(interactive=False),
            gr.update(interactive=False),
        )


def query_handler(user_msg, history):
    """
    Handle a user prompt: run agent, append result to chat.
    Returns (chatbot, textbox) updates.
    """
    if not user_msg.strip():
        return history, ""

    if current_agent is None:
        return history + [{"role": "assistant", "content": "No database connected. Please enter a valid database URL first."}], ""

    try:
        print(f"\n--- Query ---\nUser: {user_msg}")
        response = current_agent.run(user_msg)
        bot_msg = str(response.content) if response.content is not None else "(no response)"
        print(f"Agent response: {bot_msg}\n")
    except Exception as e:
        print(f"Exception type: {type(e).__name__}")
        print(f"Exception message: {e}")
        print("Full traceback:")
        print(traceback.format_exc())
        bot_msg = f"❌ Error: {e}"

    return history + [{"role": "user", "content": user_msg}, {"role": "assistant", "content": bot_msg}], ""


with gr.Blocks(title="GenAI SQL Analyst") as demo:
    gr.Markdown("# GenAI SQL Analyst")
    gr.Markdown("Connect to any SQL database and chat with it using natural language.")
    
    with gr.Row():
        db_url_input = gr.Textbox(
            placeholder="e.g., sqlite:///path/to/database.db or postgresql://user:pass@host:5432/dbname",
            label="Database URL",
            scale=4,
        )
        connect_btn = gr.Button("Connect", scale=1)
    
    status = gr.Markdown("🔌 Enter a database URL and click Connect to begin.\n\n**Examples:**\n- SQLite: `sqlite:///C:/path/to/database.db` or `sqlite:////absolute/path/database.db`\n- PostgreSQL: `postgresql://user:password@localhost:5432/dbname`\n- MySQL: `mysql+pymysql://user:password@localhost:3306/dbname`")
    chatbot = gr.Chatbot(label="Chat")
    
    with gr.Row():
        msg = gr.Textbox(
            placeholder="Ask something about your data...",
            interactive=False,
            show_label=False,
            scale=4,
        )
        send = gr.Button("Send", interactive=False, scale=1)

    connect_btn.click(
        connect_db_handler,
        inputs=[db_url_input],
        outputs=[status, chatbot, send, msg],
    )
    
    send.click(query_handler, inputs=[msg, chatbot], outputs=[chatbot, msg])
    msg.submit(query_handler, inputs=[msg, chatbot], outputs=[chatbot, msg])

demo.queue(max_size=1)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
    )

