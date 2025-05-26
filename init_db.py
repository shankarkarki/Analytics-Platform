import asyncio
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from database import create_db_and_tables, get_session, DatabaseOperations
from models import EventCreate
from datetime import datetime, timedelta
import random

