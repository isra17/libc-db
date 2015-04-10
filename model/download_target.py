from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
import datetime

Base = declarative_base()

class DownloadTarget(Base):
    __tablename__ = 'download_target'

    id =        Column(Integer, primary_key=True)

    downloaded_at = Column(DateTime, default=datetime.datetime.utcnow)

    source =    Column(String)
    md5sum =    Column(String(32))

