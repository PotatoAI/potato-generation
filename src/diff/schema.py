from sqlalchemy import Integer, String, Column, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Request(Base):
    __tablename__ = 'requests'
    id = Column(Integer(), primary_key=True)
    prompt = Column(String(200), nullable=False)
    priority = Column(Integer(), default=0)
    approved = Column(Boolean(), default=False)
    generated = Column(Boolean(), default=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(),
                        default=datetime.now,
                        onupdate=datetime.now)
    tasks = relationship("Task")
    images = relationship("Image")


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer(), primary_key=True)
    running = Column(Boolean(), default=False)
    status = Column(String(50), nullable=False, default='new')
    error = Column(Text(), nullable=True)
    priority = Column(Integer(), default=0)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(),
                        default=datetime.now,
                        onupdate=datetime.now)
    request_id = Column(Integer, ForeignKey('requests.id'))
    images = relationship("Image")


class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer(), primary_key=True)
    filename = Column(String(200), nullable=True)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(),
                        default=datetime.now,
                        onupdate=datetime.now)
    request_id = Column(Integer, ForeignKey('requests.id'))
    task_id = Column(Integer, ForeignKey('tasks.id'))
