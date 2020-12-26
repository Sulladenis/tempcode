from sqlalchemy import create_engine
import settings
from models import Base, Article, Model, Entry
from sqlalchemy.orm import sessionmaker
import re


engine = create_engine(settings.DATABASE_URI)
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()

def add_model(brand, company):
    model = Model(name=brand, company=company)
    session.add(model)
    session.commit()
    return model

def get_model(brand):
    model = session.query(Model).filter(Model.name == brand).one()
    return model

def get_article(art_id):
    return session.query(Article).get(art_id)

def search_matches(model, article):
    # id.{0,1}3
    list_matches = re.findall(model.re, article.content+article.title, re.IGNORECASE)
    return list_matches

id3 = get_model('id.3')
article = get_article(36230)
result = len(search_matches(id3, article))

if result:
    entry = Entry(model_id=id3.id, article_id=article.id, quantity=result)
