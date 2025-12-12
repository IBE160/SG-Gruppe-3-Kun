from pydantic import BaseModel
from typing import List, Dict, Any

class Chunk(BaseModel):
    content: str
    url: str
    title: str
    chunk_id: str

class QueryResult(BaseModel):
    documents: List[str]
    metadatas: List[Dict[str, Any]]