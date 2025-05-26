from fastapi import FastAPI ,Depends, Request
from pydantic import BaseModel
from typing import Dict,Any
import uvicorn
import os
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession



#import database model and functions
from models import (
    EventCreate, EventResponse , AnalyticsSummary,
    TopEventsResponse,Project, ProjectCreate , ProjectResponse
)

from database import (
    get_session,  create_db_and_tables, DatabaseOperation
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Application lifespan event handler for FastAPI """
    #create database tables
    print("Starting analytical platform application...")
    await create_db_and_tables()

    #yield control to the application
    yield

    #cleanup actions if any
    print("Application shutdown complete.")



#create a FastAPI instance
app = FastAPI(
    title = "FastAPI Example",
    description = "Real time event analytics platform",
    version = "1.0.0",
    lifespan = lifespan,
)
    

@app.get("/")
async def read_root():
    """ Health Check Endpoint
    """
    return {"message": "Welcome to the FastAPI Event Analytics Platform! ",
            "version" : "1.0.0",
            "database": "Connected" if os.getenv("DATABASE_URL") else "Not Connected"}


@app.post("/events/" , response_model = dict)
async def create_event(
    event: EventCreate,
    request : Request,
    session:AsyncSession = Depends(get_session)):
    """
      Creating a new event with database persistence
    """
    try:
        db_ops = DatabaseOperation(session)

        #get client metadata
        ip_address = request.client.host
        user_agent = request.headers.get("User-Agent", "Unknown")
   
        #create event in the database
        event_response = await db_ops.create_event(
            event_data=event_data,
            ip_address=ip_address,
            user_agent=user_agent
        )


        return {
               "status": "success",
                "message": "Event created successfully",
                "event_id": event_response.id,
                "timestamp": event_response.timestamp.isoformat(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating event: {str(e)}"
        )





@app.get("/events/",response_model=dict)
async def get_events(
    limit:int =10,
    offset:int = 0,
    session: AsyncSession = Depends(get_session)
):
    """ Get recent event with pagination
    """
    try:
        db_ops = DatabaseOperation(session)
        events = await db_ops.get_events(limit=limit, offset=offset)
        total_count = await db_ops.get_total_events_count()

        return {
            "totalevents": total_count,
            "limit": limit,
            "offset": offset,
            "events": [
                {
                    "id": event.id,
                    "event_name": event.event_name,
                    "user_id": event.user_id,
                    "session_id": event.session_id,
                    "timestamp": event.timestamp.isoformat(),
                    "properties": event.properties,
                    "user_properties": event.user_properties,
                    "ip_address": event.ip_address,
                    "user_agent": event.user_agent,
                } for event in events
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching events: {str(e)}"
        )
   


@app.get("/analytics/summary/" , response_model=AnalyticsSummary)
async def get_analytics_summary(
    session: AsyncSession = Depends(get_session),
):
    """ Get analytics summary
    """
    try:
        db_ops = DatabaseOperation(session)
        total_events = await db_ops.get_event_count()
        unique_users = await db_ops.get_unique_users_count()
        unique_sessions = await db_ops.get_unique_sessions_count()
        data_range = await db_ops.get_data_range()

        return {
        "total_events": "Analytics summary",
        "unique_users": len(events_store),
        "unique_sessions": unique_users,
        "data_range": events_type
    }

    except Exception as ex:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching analytics summary: {str(ex)}"
        )
    

@app.get("/events/top/", response_model= list[TopEventsResponse])
async def get_top_events(
    limit: int = 10,
    session: AsyncSession = Depends(get_session)
):
    """ Get top events by count
    """
    try:
        db_ops = DatabaseOperation(session)
        top_events = await db_ops.get_top_events(limit=limit)
        
        return [TopEventsResponse(**event) for event in top_events]
        

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching top events: {str(e)}"
        )
    
# Error handlers
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """ Global General exception handler for the application """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc),
            "path": str(request.url),}
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
 