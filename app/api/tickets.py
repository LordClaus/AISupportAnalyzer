from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketResponse
from app.services.ai_analyzer import analyze_ticket_text

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("/", response_model=TicketResponse)
async def create_and_analyze_ticket(
        request: TicketCreate,
        db: AsyncSession = Depends(get_db)
):
    try:
        ai_result = await analyze_ticket_text(request.text)

        new_ticket = Ticket(
            customer_text=request.text,
            category=ai_result.get("category"),
            priority=ai_result.get("priority"),
            suggested_response=ai_result.get("suggested_response"),
        )

        db.add(new_ticket)
        await db.commit()
        await db.refresh(new_ticket)

        return new_ticket

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))