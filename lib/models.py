from sqlalchemy import Column, Integer, String, Text, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import scoped_session, sessionmaker
from app.lib.databaseConfig import DATABASE

# Create DB Engine
Base = declarative_base()
engine = create_engine(URL(**DATABASE))
db_session = scoped_session(sessionmaker(autocommit=False,
                                     autoflush=False,
                                     bind=engine))

Base.query = db_session.query_property()

# Set Schema Name
schema_name = 'public'

# Create our database model
class events(Base):
    __tablename__ = 'events'
    __table_args__ = {"schema": schema_name}
    row = Column(Integer, primary_key=True)
    eventDate = Column(Date)
    eventTimestamp = Column(DateTime)
    userid = Column(String(120))
    campaignId = Column(String(120))
    eventname = Column(String(120))
    versionName = Column(String(120))
    usercountry = Column(String(120))
    device = Column(String(120))
    amount = Column(String(120))
    levelNumber = Column(String(20))
    item = Column(String(120))

    def __init__(self, row=None, eventDate=None, eventTimestamp=None, userid=None, campaignId=None, eventname=None, versionName=None, usercountry=None, device=None, amount=None, levelNumber=None, item=None):
        self.row = row
        self.eventDate = eventDate
        self.eventTimestamp = eventTimestamp
        self.userid = userid
        self.campaignId = campaignId
        self.eventname = eventname
        self.versionName = versionName
        self.usercountry = usercountry
        self.device = device
        self.amount = amount
        self.levelNumber = levelNumber
        self.item = item
