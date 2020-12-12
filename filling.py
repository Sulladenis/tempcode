from sqlalchemy import create_engine
import settings
from models import Base
from sqlalchemy.orm import sessionmaker
import re

#Article, Model, Entry,

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
    content = article.content
    content = 'id3, id 3,'
    list_matches = re.findall('id.{0,1}3', content, re.IGNORECASE)
    return list_matches


#id3 = get_model('id.3')
#article = get_article(36430)
#result = search_matches(id3, article, )

# todo: Загрузить экзкмпляр марки -> obj
# todo: Загрузить зкземпляр страницы -> obj
# todo: Найти количество упоменаний марки в странице -> int
# todo: Создать экземпляр вхождений (entry) -> obj

