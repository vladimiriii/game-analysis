import os
import sys
from datetime import datetime
import configparser
from pathlib import Path

# SQL Alchemy
from sqlalchemy import Column, Integer, String, Text, DateTime, Date
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Database Config
from app.lib.databaseConfig import DATABASE

# Database Models
import app.lib.models as md

# Creates the DB engine
engine = create_engine(URL(**DATABASE))

# Drop Old Tables
drop_query = ( 'DROP TABLE events;')
engine.execute(drop_query)
# md.Base.metadata.drop_all(bind=engine)#, tables=[md.subcategory, md.category, md.rating, md.comment, md.view, md.sheet, md.app_user, md.app_user_role])

# Create New Table
md.Base.metadata.create_all(bind=engine)
