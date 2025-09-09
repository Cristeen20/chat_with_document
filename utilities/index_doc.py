
import os
import tempfile
import shutil
import faiss

from llama_index.core import SimpleDirectoryReader,Settings
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.faiss import FaissVectorStore
from utilities.embedding import LlamaEmbedder
from utilities.llm_client import llm

embedder = LlamaEmbedder()
Settings.embed_model = embedder
Settings.llm =  llm

def index_document(file_path,uu_id="000"):
    """
    Index a document for search.
    Args:
        file_path (str): The path to the document to be indexed.
    Returns:
        bool: True if indexing was successful, False otherwise.
    """

    tmp = tempfile.gettempdir()
    folder_name = "indexed_docs"
    dest_folder = os.path.join(tmp,folder_name)
    os.makedirs(dest_folder, exist_ok=True)
    destination = os.path.join(dest_folder, os.path.basename(file_path))
    
    shutil.copy(file_path, destination)
    
    
    
    filename_fn = lambda file_path: {"file_path":file_path, "uu_id":uu_id}
    documents = SimpleDirectoryReader(
                            dest_folder,
                            file_metadata = filename_fn
                        ).load_data()
    store_index(documents)
    shutil.rmtree(dest_folder)
    return {"index_status": True}



def store_index(documents):
    """
    Store the index to disk.
    Args:
        documents (List[Document]): The documents to be indexed.
    Returns:
        bool: True if storing was successful, False otherwise.
    """
    
    # dimensions of text-ada-embedding-002
    d = 768
    faiss_index = faiss.IndexFlatL2(d)

    vector_store = FaissVectorStore(faiss_index=faiss_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context,show_progress=True)
    index.storage_context.persist()

    print("Storing index...")
    return True