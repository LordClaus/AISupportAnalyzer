from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.db.session import get_db
from app.models.ticket import Ticket
from app.services.ai_analyzer import analyze_ticket_text

router = APIRouter()


class TicketCreateRequest(BaseModel):
    text: str


class TicketResponse(BaseModel):
    id: int
    customer_text: str
    category: str
    priority: str
    status: str


@router.post("/tickets/", response_model=TicketResponse)
async def create_and_analyze_ticket(
        request: TicketCreateRequest,
        db: AsyncSession = Depends(get_db)
):
    ai_result = await analyze_ticket_text(request.text)

    new_ticket = Ticket(
        customer_text=request.text,
        category=ai_result.category,
        priority=ai_result.priority,
        suggested_response=ai_result.suggested_response
    )

    db.add(new_ticket)
    await db.commit()
    await db.refresh(new_ticket)

    return new_ticket