from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import gradio as gr
import os
from html_string import main_html, plain_html
# from upload_file import *
# from create_kb import *
from chat import get_model_response, update_knowledge_base, clear_tmp

DB_PATH = "vectordb"


def user(user_message, history):
    print(user_message)
    return {'text': '', 'files': user_message['files']}, history + [[user_message['text'], None]]

def get_chat_block():
    with gr.Blocks(
        theme=gr.themes.Base(), 
        css=".gradio_container { background-color: #f0f0f0; }") as chat:
        gr.HTML(plain_html)

        with gr.Row():
            # Main chat window
            with gr.Column(scale=10):
                chatbot = gr.Chatbot(
                    label="Chatbot",
                    height=750,
                    avatar_images=("images/user.jpeg", "images/tongyi.png")
                )
                with gr.Row():
                    # Input
                    input_message = gr.MultimodalTextbox(
                       label = "Please input",
                       file_types = [".xlsx", ".csv", ".docx", ".pdf", ".txt"],
                       scale=7
                    )
                    clear_btn = gr.ClearButton(chatbot, input_message, scale=1)

            with gr.Column(scale=5):
                knowledge_base = gr.Dropdown(
                    choices=os.listdir(DB_PATH),
                    label="Load KB",
                    interactive=True,
                    scale=2
                )

                with gr.Accordion(label="Recall text", open=False):
                    chunk_text = gr.Textbox(
                        label="Recall text",
                        interactive=False,
                        scale=5,
                        lines=10
                    )

                with gr.Accordion(label="Model config", open=True):
                    model = gr.Dropdown(
                        choices=['qwen-max', 'qwen-plus', 'qwen-turbo', 'gpt-4o-mini'],
                        label="Select Model",
                        interactive=True,
                        value="qwen-max",  # Default to strongest model
                        scale=2
                    )

                    temperature = gr.Slider(
                        maximum=2, minimum=0,
                        interactive=True,
                        label="Temperature",
                        step=0.01,
                        value=0.85,
                        scale=2
                    )

                    max_tokens = gr.Slider(
                        maximum=2000, minimum=0,
                        interactive=True,
                        label="Max Response Length",
                        step=50,
                        value=1024,
                        scale=2
                    )

                    history_round = gr.Slider(
                        maximum=30, minimum=1,
                        interactive=True,
                        label="Context Rounds",
                        step=1,
                        value=3,  # Balance context understanding and token consumption
                        scale=2
                    )

                with gr.Accordion(label="RAG parameters", open=True):
                    chunk_cnt = gr.Slider(
                        maximum=20, minimum=1,
                        interactive=True,
                        label="Number of Retrieved Chunks",
                        step=1,
                        value=5,  # Balance information completeness and processing efficiency
                        scale=2
                    )
                    # Similarity threshold - filter low relevance documents
                    similarity_threshold = gr.Slider(
                        maximum=1, minimum=0,
                        interactive=True,
                        label="Similarity Threshold",
                        step=0.01,
                        value=0.2,  # Lower threshold ensures recall coverage
                        scale=2
                    )
        # 事件绑定 - 实现响应式交互
        # 链式调用：用户输入 -> 消息预处理 -> 模型响应生成
        input_message.submit(
            fn=user,
            inputs=[input_message, chatbot],
            outputs=[input_message, chatbot],
            queue=False # 禁用队列确保实时响应
        ).then(
            fn=get_model_response,
            inputs=[input_message, chatbot, model, temperature, max_tokens,
                    history_round, knowledge_base, similarity_threshold, chunk_cnt],
            outputs=[chatbot, chunk_text]
        )

        # 页面加载时的初始化操作
        chat.load(update_knowledge_base, [], knowledge_base)
        chat.load(clear_tmp)

    return chat

app = FastAPI()
@app.get("/", response_class=HTMLResponse)
def read_main():
    """
    Root endpoint that serves the main HTML page.
    
    Returns:
        HTMLResponse: The main HTML content for the application's homepage.
    """
    html_content = main_html
    return HTMLResponse(content=html_content)



app = gr.mount_gradio_app(app, get_chat_block(), path="/chat")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7866, reload=True)
