from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict,Any
import uvicorn

#create a FastAPI instance
app = FastAPI(
    title="FastAPI Example",
    description="Real time event analytics platform",
    version="1.0.0",
)

#simple event model
class Event(BaseModel):
    event_name: str
    user_id: str =None
    properties: Dict[str, Any] = {}
    

#In-memory storage for events
events_store = []

@app.get("/")
async def read_root():
    """ Health Check Endpoint
    """
    return {"message": "Welcome to the FastAPI Event Analytics Platform! version 1.0.0"}

@app.post("/events/")
async def create_event(event: Event):
    """ Simple event ingestion endpoint
    """

    #for now lets store in memory
    event_data = event.dict()
    event_data["event_id"] = len(events_store) + 1
    events_store.append(event_data)

    return {"message": "Event created successfully", 
            "event_id": event_data["event_id"],}

@app.get("/events/")
async def get_events():
    """ Get all events
    """
    return {
        "total_events": len(events_store),
        "events": events_store[-10:]
        }

@app.get("/analytics/summary/")
async def get_analytics_summary():
    """ Get analytics summary
    """
    if not events_store:
        return {
            "message": "No events found",
            "total_events": 0,
            "unique_users": 0,
            "events_type": {}
            }
    unique_users = len(set(event["user_id"] for event in events_store if event["user_id"]))


    #count events by type
    events_type = {}
    for event in events_store:
        event_name = event.get("event_name", "unknown")
        events_type[event_name] = events_type.get(event_name, 0) + 1

    return {
        "message": "Analytics summary",
        "total_events": len(events_store),
        "unique_users": unique_users,
        "events_type": events_type
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
 