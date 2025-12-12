from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional

class UserRole(str, Enum):
    CONSTRUCTION_WORKER = "Construction Worker"
    SUPPLIER_SUBCONTRACTOR = "Supplier / Subcontractor"
    PROJECT_MANAGER_ADMIN = "Project Manager / Admin"

class ChatRequest(BaseModel):
    message: str
    user_role: Optional[UserRole] = None

class SourceCitation(BaseModel):
    title: str
    url: str

class ChatResponse(BaseModel):
    answer: str
    citations: List[SourceCitation] = []
    confidence: Optional[float] = None
    fallback_message: Optional[str] = None