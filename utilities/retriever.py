


from llama_index.core import load_index_from_storage, StorageContext
from llama_index.vector_stores.faiss import FaissVectorStore

def retrive_index():
    """
    Retrieve the index from storage.
    Returns:
        query_engine: The query engine to fetch answers.
    """
    vector_store = FaissVectorStore.from_persist_dir("./storage")
    storage_context = StorageContext.from_defaults(vector_store=vector_store, persist_dir="./storage")
    index = load_index_from_storage(storage_context=storage_context)
    query_engine = index.as_query_engine()

    if query_engine:
        return query_engine