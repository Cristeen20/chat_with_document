import asyncio
import torch
import numpy as np
from typing import List
from pydantic import Field
from transformers import AutoTokenizer, AutoModel
from llama_index.core.base.embeddings.base import BaseEmbedding


class BGEEmbedding():
    def __init__(self, device='cpu', base_path: str = '') -> None:
        self.device = device
        self.base_path = base_path
        if not self.base_path:
            self.base_path = "BAAI/bge-base-en-v1.5"
        self.tokenizer = AutoTokenizer.from_pretrained(self.base_path)
        self.model = AutoModel.from_pretrained(self.base_path).to(self.device)
        self.model.eval()

    def embed(self, text: str) -> list[float]:

        inputs = self.tokenizer([text], padding=True, return_tensors='pt', max_length=512, truncation=True).to(self.device) 
        with torch.no_grad():
            outputs = self.model(**inputs)
            batch = outputs.last_hidden_state[:, 0]
            batch = torch.nn.functional.normalize(batch, p=2, dim=1)
            return np.array(batch.tolist()[0])
        

class LlamaEmbedder(BaseEmbedding):
    embedder: "BGEEmbedding" = Field(default=None, exclude=True)
    def __init__(self, device='cpu', base_path=''):
        super().__init__()
        object.__setattr__(self, 'embedder', BGEEmbedding(device=device, base_path=base_path))
        

    def embed(self, text: str) -> List[float]:  # Add this method
        return self.embedder.embed(text)

    def _get_text_embedding(self, text: str) -> List[float]:
        return self.embedder.embed(text)

    def _get_query_embedding(self, query: str) -> List[float]:
        return self.embedder.embed(query)

    async def _aget_query_embedding(self, query: str) -> List[float]:
        # Run the sync method in a thread pool for async compatibility
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._get_query_embedding, query)

   
    
    

