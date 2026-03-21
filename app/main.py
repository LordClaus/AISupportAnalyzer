from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db, engine
from app.db.base import Base
from app.schemas.ticket import TicketCreate, TicketResponse
from app.services.ai_analyzer import analyze_ticket_text
from app.api.tickets import router as tickets_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="AI Support Analyzer", lifespan=lifespan)

app.include_router(tickets_router)


@app.get("/")
async def root():
    return {"message": "База даних підключена, ШІ готовий!"}


@app.post("/analyze", response_model=TicketResponse)
async def create_ticket(request: TicketCreate = Body(...), db: AsyncSession = Depends(get_db)):
    try:
        ai_data = await analyze_ticket_text(request.text)

        from app.models.ticket import Ticket
        new_ticket = Ticket(
            customer_text=request.text,
            category=ai_data.get("category"),
            priority=ai_data.get("priority"),
            suggested_response=ai_data.get("suggested_response")
        )

        db.add(new_ticket)
        await db.commit()
        await db.refresh(new_ticket)

        return new_ticket

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))