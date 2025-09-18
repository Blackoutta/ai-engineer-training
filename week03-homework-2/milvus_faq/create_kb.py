import gradio as gr
import os
import shutil
from llama_index.core import VectorStoreIndex, Settings, SimpleDirectoryReader
from llama_index.embeddings.openai import OpenAIEmbedding

EMBED_MODEL = OpenAIEmbedding(
    model="text-embedding-3-small",  # or "text-embedding-3-large", "text-embedding-ada-002"
    embed_batch_size=10,  # optional: batch size for embedding requests
)

from llama_index.core.schema import TextNode
from upload_file import *