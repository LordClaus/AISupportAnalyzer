from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class TicketCreate(BaseModel):
    text: str = Field(..., example="В мене не працює кнопка оплати")

class TicketResponse(BaseModel):
    id: int
    customer_text: str
    category: Optional[str] = None
    priority: Optional[str] = None
    suggested_response: Optional[str] = None
    status: str

    model_config = ConfigDict(from_attributes=True)