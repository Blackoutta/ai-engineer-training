import os
from typing import Callable, List
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.schema import Document, BaseNode
from llama_index.core.node_parser import TokenTextSplitter, SentenceSplitter, SentenceWindowNodeParser
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.openai import OpenAIEmbedding
from dotenv import load_dotenv

# Config logging
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger("llama_index").addHandler(logging.StreamHandler(stream=sys.stdout))

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


def build_nodes(documents: List[Document]) -> List[BaseNode]:
    splitter = TokenTextSplitter(
        chunk_size=200,
        chunk_overlap=10,
        separator="\n"
    )
    return splitter.get_nodes_from_documents(documents)

def build_sentence_nodes(documents: List[Document]) -> List[BaseNode]:
    splitter = SentenceSplitter(
        chunk_size=200,
        chunk_overlap=10,
        separator="\n"
    )
    return splitter.get_nodes_from_documents(documents)

def build_sentence_window_nodes(documents: List[Document]) -> List[BaseNode]:
    splitter = SentenceWindowNodeParser(
        window_size=3,
        window_metadata_key="window",
        original_text_metadata_key="original_text"
    )
    return splitter.get_nodes_from_documents(documents)


def get_documents(data_dir: str = "data") -> List[Document]:
    return SimpleDirectoryReader(data_dir).load_data()


def run_query_over_nodes(build_fn: Callable[[List[Document]], List[BaseNode]],
                         documents: List[Document],
                         prompt: str) -> str:
    nodes = build_fn(documents)
    index = VectorStoreIndex(nodes)
    response = index.as_query_engine().query(prompt)
    return str(response)


def main() -> None:
    configure_settings()
    documents = get_documents("data")
    prompt = "What is earthquake, answer in 50 words"

    strategies: List[tuple[str, Callable[[List[Document]], List[BaseNode]]]] = [
        ("token", build_nodes),
        ("sentence", build_sentence_nodes),
        ("sentence_window", build_sentence_window_nodes),
    ]

    for name, builder in strategies:
        print(f"\n--- Strategy: {name} ---")
        print(run_query_over_nodes(builder, documents, prompt))

if __name__ == "__main__":
    main()
