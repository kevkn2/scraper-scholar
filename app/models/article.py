from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from app.domain.entities.scholar.crawl_result import ScholarData
from app.models.base_model import Base


class ArticleModel(Base):
    __tablename__ = "articles"

    id = Column(String, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    url = Column(String(2048), unique=True, nullable=False)
    authors = Column(String(1000), nullable=False)  # Comma-separated author names
    year = Column(Integer, nullable=True)
    pdf_url = Column(String(2048), nullable=True)
    citations_url = Column(String(2048), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dto(self) -> ScholarData:
        """Convert to ScholarData DTO"""

        return ScholarData(
            title=self.title,
            authors=[a.name for a in self.authors.split(",")],
            url=self.url,
            year=self.year,
            pdf_url=self.pdf_url,
            citations_url=self.citations_url,
        )
