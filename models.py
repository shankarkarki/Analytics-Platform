"""
Database models based on SQLModel
"""

from datetime import datetime
from typing import Dict , Optional, Any
from sqlmodel import Field, SQLModel, Column , JSON
from sqlalchemy import func , DateTime

class EventBase(SQLModel):
    """ Base model for API request/response """

    event_name: str = Field(max_length=255, description="Name of the event")
    user_id: Optional[str] = Field(default=None, max_length=255, description="User Identifier")
    session_id : Optional[str] = Field(default=None, max_length=255, description="Session Identifier")
    properties: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON) , description="Event properties ")
    user_properties: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON) , description="User properties")



class Event(EventBase, table=True):
    """ Event  table model """
    __tablename__ = "events"

    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp : datetime = Field(
        default_factory=datetime.utcnow, 
        sa_column=Column(DateTime(timezone=True),server_default=func.now()),
        description="Event timestamp")
    
    #Meta data fields
    ip_address: Optional[str] = Field(default=None, max_length=45, description="IP Address of the user")
    user_agent: Optional[str] = Field(default=None, max_length=512, description="User Agent of the user")

    # processing metadata
    created_at: datetime = Field(
        default_factory=datetime.utcnow, 
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

class EventCreate(EventBase):
    """ Event creation model for API request """
    timestamp: Optional[datetime] = None


class EventResponse(EventBase):
    """ Event response model for API response """
    user_id : int
    timestamp : datetime
    created_at: datetime
    ip_address: Optional[str] = None


class ProjectBase(SQLModel):
    """ Base model for Project """
    name: str = Field(max_length=255, description="Project name")
    slug :str = Field(max_length=255, description="Project slug/identifier")
    description: Optional[str] = Field(default=None, max_length=1024, description="Project description")
    isactive: bool = Field(default=True, description="Is the project active")

class Project(ProjectBase, table=True):
    """ Project table model """
    __tablename__ = "projects"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow, 
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, 
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )

    #Project Settings
    event_retention_days: int = Field(default=90, description="Number of days to retain events")
    monthly_event_limit: int = Field(default=10000, description="Monthly event limit")

class ProjectCreate(ProjectBase):
    """ Project creation model for API request """
    pass

class ProjectResponse(ProjectBase):
    """ Project response model for API response """
    id: int
    created_at: datetime
    event_retention_days: int
    monthly_event_limit: int

# Anlaytics Response Model not the db table
class AnalyticsSummary(SQLModel):
    """ Analytics summary response model """
    total_events: int = Field(description="Total number of events")
    unique_users: int = Field(description="Number of unique users")
    unique_sessions: int = Field(description="Number of unique sessions")
    events_type: Dict[str, int] = Field(default_factory=dict, description="Events count by type")
    data_range: Dict[str, datetime] = Field(description="Date range of the events")

class EventCountByDate:
    date: datetime = Field(description="Date of the event")
    count: int = Field(description="Number of events on that date")


class AnalyticsTimeSeriesResponse:
    """ Analytics time series response model """
    period: str = Field(description="Time period for the data ( day , hour)")
    data:list[EventCountByDate] = Field(description="Time Series DataPoints")
    total_events: int = Field(description="Total number of events in the time series")

class TopEventsResponse:
    """ Top events response model """
    event_name: str = Field(description="Name of the event")
    count :int = Field(description="Count of the event")
    unique_users: int = Field(description="Number of unique users")
    percentage: float = Field(description="Time range of the top events")
    