from sqlalchemy import Integer, String, Column, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import OID
from datetime import datetime

Base = declarative_base()


class Request(Base):
    __tablename__ = 'requests'
    id = Column(Integer(), primary_key=True)
    prompt = Column(Text(), nullable=False)
    priority = Column(Integer(), default=0)
    approved = Column(Boolean(), default=False)
    generated = Column(Boolean(), default=False)
    kind = Column(String(100), nullable=False, default='unknown')
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(),
                        default=datetime.now,
                        onupdate=datetime.now)
    images = relationship("Image",
                          cascade="all, delete",
                          backref="request",
                          passive_deletes=True)
    videos = relationship("Video",
                          cascade="all, delete",
                          backref="request",
                          passive_deletes=True)


class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer(), primary_key=True)
    filename = Column(String(200), nullable=True)
    selected = Column(Boolean(), default=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(),
                        default=datetime.now,
                        onupdate=datetime.now)
    request_id = Column(Integer, ForeignKey('requests.id', ondelete='CASCADE'))
    oid = Column(OID)
    hqoid = Column(OID)


class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer(), primary_key=True)
    filename = Column(String(200), nullable=True)
    selected = Column(Boolean(), default=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(),
                        default=datetime.now,
                        onupdate=datetime.now)
    request_id = Column(Integer, ForeignKey('requests.id', ondelete='CASCADE'))
    oid = Column(OID)
