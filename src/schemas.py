from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import date


#pydantic model for input validation
class TransactionCreate(BaseModel):
    amount: float = Field(gt=0)
    date: date
    category: str
    type: Literal["income", "expense"]
    description: Optional[str] = None
