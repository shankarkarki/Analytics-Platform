"""
Database Connection and Session Manager
"""

import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from models import Event, Project


# Database URL from the environment variable
DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

#creating async engine
engine = create_async_engine(
    DATABASE_URL,
    echo = True,    # setting to false in  production
    future = True
)


#Create async session factory 
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit= False
)


async def create_db_and_tables():
    """Create database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[ç,None]:
    """get database session for fastapi dependency"""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()




# Database Operation

class DatabaseOperation:
    """ Database Operation for analytics platform """

    def __init__(self,session:AsyncSession):
        self.session = session 


    async def create_event(self , 
                           event_data:dict , ip_adress:str = None , 
                           user_agent:str= None)-> Event:
        """Create new Event in the database """
        event = Event(
            **event_data,
            ip_address=ip_adress,
            user_agent=user_agent
        )

        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event
    
    async def get_events(self, limit: int = 100, offset: int = 0) -> list[Event]:
        """Get events from the database with pagination"""
        from sqlalchemy import select , desc

        query = select(Event).order_by(desc(Event.timestamp)).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_event_count(self) -> int:
        """Get total event count"""
        from sqlalchemy import select, func

        query = select(func.count(Event.id))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_unique_users_count(self) -> int:
        """Get count of unique users"""
        from sqlalchemy import select, func

        query = select(func.count(func.distinct(Event.user_id)))
        result = await self.session.execute(query)
        return result.scalar_one_or_none() or 0
    
    async def get_unique_sessions_count(self) -> int:
        """Get count of unique users"""
        from sqlalchemy import select, func

        query = select(func.count(func.distinct(Event.session_id))).where (Event.session_id.is_not(None))
        result = await self.session.execute(query)
        return result.scalar_one_or_none() or 0
    
    async def get_events_by_type(self) -> dict[str,int]:
        """Get count of events by type"""
        from sqlalchemy import select, func

        query = select(Event.event_name, func.count(Event.id)).group_by(Event.event_name)
        result = await self.session.execute(query)
        return {row[0]: row[1] for row in result.all()}
    
    async def get_data_range(self) -> dict:
        """Get date range of events"""
        from sqlalchemy import select, func

        query = select(func.min(Event.timestamp), func.max(Event.timestamp))
        result = await self.session.execute(query)
        min_date, max_date = result.first()
        return {
            "start_date": min_date,
            "end_date": max_date
        }
    
    async def get_events_by_data_range(self,start_date,end_date,limit:int = 1000)-> list[Event]: 
    
        """Get events within a specific date range"""
        from sqlalchemy import select

        query = select(Event).where(
            Event.timestamp >= start_date,
            Event.timestamp <= end_date
        ).limit(limit)
        
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_top_events(self,limit:int=10) -> list[dict]:
        """Get top events by count"""
        from sqlalchemy import select, func

          # Get total event count for percentage calculation

        total_query = select(func.count(Event.id))
        total_result = await self.session.execute(total_query)  
        total_events = total_result.scalar()

        # get top events
        query = select(
            Event.event_name,
                func.count(Event.id).label("count"),
                func.count(func.distinct(Event.user_id)).label("unique_user")
            ).group_by(Event.event_name).order_by(func.count(Event.id).desc()).limit(limit)

        result = await self.session.execute(query)

        top_events = []
        for row in result.all():
            event_name, count ,unique_user = row
            percentage = (count / total_events * 100) if total_events else 0
            top_events.append({
                "event_name": event_name,
                "count": count,
                "unique_user": unique_user or 0,
                "percentage": round(percentage,0)
            })

        return top_events