import os
from openai import OpenAI
from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.embeddings.openai import OpenAIEmbedding

# Reranking module import - using graceful degradation strategy
try:
    from llama_index.postprocessor.cohere_rerank import CohereRerank
except ImportError:
    print("Warning: CohereRerank not found, will skip reranking")
    CohereRerank = None
    # Design philosophy: system can still work normally when reranking component is missing
    # Implement graceful degradation through None value marking and conditional checks

from create_kb import *
