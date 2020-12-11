from concurrent.futures import ThreadPoolExecutor, as_completed
from sqlalchemy import select, create_engine
from sqlalchemy.orm import sessionmaker
import settings
from models import Base, Article
from urls import get_urls
from scrape import Page


class manager:

    def __init__(self):
        self.all_urls = set()
        self.engine = create_engine(settings.DATABASE_URI)
        self.urls_db = self.select_all_urls()
        self.session = sessionmaker(bind=self.engine)()

    def gen_url(self):
        num = 1
        while True:
            yield settings.URL+f'/?p={num}'
            num += 1

    def select_all_urls(self):
        with self.engine.connect() as conn:
            table = Base.metadata.sorted_tables[0]
            data = conn.execute(select([table.c.url]))
            urls = [row.url for row in data]
            return set(urls)

    def in_section(self, urls):
        return self.urls_db.intersection(urls)

    def load_urls(self):
        gen_url = self.gen_url()
        while True:
            url = next(gen_url)
            urls_page = get_urls(url)
            intersection = self.in_section(urls=urls_page)
            print(url, len(intersection))
            self.all_urls.update(urls_page)
            if len(intersection) >= 20:
                break
        self.all_urls -= self.urls_db

    def scraping_page(self, url: str) -> object:
        page = Page(url)
        return page

    def insert_article(self, page):
        article = Article(
            url=page.url,
            date=page.date,
            title=page.title,
            content=page.content
        )
        self.session.add(article)
        self.session.commit()

    def load_data(self):
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(self.scraping_page, url): url for url in self.all_urls}
            for num, future in enumerate(as_completed(future_to_url)):
                url = future_to_url[future]
                try:
                    page = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (url, exc))
                else:
                    self.insert_article(page)
                    print(f'{num + 1} is {len(self.all_urls)}')
                finally:
                    self.session.close()


if __name__ == '__main__':
    manager = manager()
    manager.load_urls()
    manager.load_data()




