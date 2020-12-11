from sqlalchemy import Column, Integer, String, ForeignKey, DATE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    date = Column(DATE)
    title = Column(String)
    content = Column(String)
    entry = relationship("Entry", back_populates="article")


class Model(Base):
    __tablename__ = 'model'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    company = Column(String)
    entry = relationship("Entry", back_populates='model')


class Entry(Base):
    __tablename__ = 'entry'
    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey('model.id'))
    model = relationship("Model", back_populates="entry")
    quantity = Column(Integer)
    article_id = Column(Integer, ForeignKey('article.id'))
    article = relationship("Article", back_populates="entry")
