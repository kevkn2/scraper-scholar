from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    func,
    Index,
)

from app.models.base_model import Base


class OAuthTokenModel(Base):
    __tablename__ = "oauth_tokens"

    id = Column(String, primary_key=True)  # UUID or provider-based ID
    provider = Column(String(50), nullable=False, unique=True)

    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=True)

    expires_at = Column(DateTime(timezone=True), nullable=False)
    scope = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (Index("ix_oauth_tokens_provider", "provider"),)

    def is_expired(self) -> bool:
        return datetime.utcnow() >= self.expires_at
