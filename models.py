from pydantic import BaseModel, Field
from typing import List, Optional

class PessoaCreate(BaseModel):
    nome: str
    data_de_nascimento: str = Field(..., description="Formato data, ex: 1990-01-01")
    cpf: str
    telefone: str
    data: str = Field(..., description="Formato datetime, ex: 2026-09-18T10:00:00Z")
    sexo: str
    hobbies: List[str]
    cidade: Optional[List[str]] = []

class PhaseUpdate(BaseModel):
    phase_id: int
