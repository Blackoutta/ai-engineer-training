from paddlex import create_pipeline
from image_ocr_reader import ImageOCRReader
from audioop import avg
from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document
import os
from typing import List, Union
from paddlex import create_pipeline
from llama_index.core import Settings
from dotenv import load_dotenv
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.schema import Document, BaseNode
from llama_index.core.node_parser import TokenTextSplitter, SentenceSplitter, SentenceWindowNodeParser
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.openai import OpenAIEmbedding
from typing import Callable, List

load_dotenv()

def configure_settings() -> None:
    Settings.llm = OpenAILike(
        model="gpt-4o-mini",
        is_chat_model=True
    )

    Settings.embed_model = OpenAIEmbedding(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY"),
        api_base=os.getenv("OPENAI_API_BASE"),
    )

def build_sentence_window_nodes(documents: List[Document]) -> List[BaseNode]:
    splitter = SentenceWindowNodeParser(
        window_size=3,
        window_metadata_key="window",
        original_text_metadata_key="original_text"
    )
    return splitter.get_nodes_from_documents(documents)


def run_query_over_nodes(build_fn: Callable[[List[Document]], List[BaseNode]],
                         documents: List[Document],
                         prompt: str) -> str:
    nodes = build_fn(documents)
    index = VectorStoreIndex(nodes)
    response = index.as_query_engine().query(prompt)
    return str(response)

def main():
    ocr = ImageOCRReader()
    docs = ocr.load_data(["./data/test1.png", "./data/test2.png"])
    configure_settings()
    prompt = "What's in the image?"

    print(run_query_over_nodes(build_sentence_window_nodes, docs, prompt))
    

if __name__ == "__main__":
    main()
