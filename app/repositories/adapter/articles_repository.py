from typing import List
import uuid

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from app.domain.entities.scholar.crawl_result import ScholarData
from app.models.article import ArticleModel
from app.repositories.interfaces import IArticlesRepository
from sqlalchemy.ext.asyncio import AsyncSession


class ArticlesRepository(IArticlesRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_articles(self, articles: List[ScholarData]) -> List[ArticleModel]:
        """Upsert articles in batch using ON CONFLICT"""
        if not articles:
            return []

        try:
            # Prepare article data
            article_data = [
                {
                    "id": uuid.uuid4().hex,
                    "title": article.title,
                    "url": article.url,
                    "year": article.year,
                    "pdf_url": article.pdf_url,
                    "citations_url": article.citations_url,
                    "authors": ",".join([a for a in article.authors]),
                }
                for article in articles
            ]

            # PostgreSQL upsert
            stmt = insert(ArticleModel).values(article_data)
            stmt = stmt.on_conflict_do_update(
                index_elements=["url"],
                set_={
                    "title": stmt.excluded.title,
                    "year": stmt.excluded.year,
                    "pdf_url": stmt.excluded.pdf_url,
                    "citations_url": stmt.excluded.citations_url,
                },
            )

            await self.session.execute(stmt)
            await self.session.commit()

            # Fetch and return upserted articles
            urls = [article.url for article in articles]
            result = await self.session.execute(
                select(ArticleModel).where(ArticleModel.url.in_(urls))
            )
            return result.scalars().all()

        except Exception as e:
            await self.session.rollback()
            raise ValueError(f"Failed to upsert articles: {str(e)}")

    async def search_article_by_title(self, title: str) -> List[ScholarData]:
        results = await self.session.execute(
            select(ArticleModel).where(ArticleModel.title.ilike(f"%{title}%"))
        )
        articles = results.scalars().all()
        return [ScholarData(**article.dict()) for article in articles]


def new_articles_repository(session: AsyncSession) -> IArticlesRepository:
    return ArticlesRepository(session=session)
