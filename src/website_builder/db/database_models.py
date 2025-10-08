import uuid
from typing import Optional

import sqlalchemy as sa
from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from website_builder.db.database import Base


class Session(Base):
    __tablename__ = "session"

    id: Mapped[str] = mapped_column(
        sa.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    requirement_gatherer_output: Mapped[Optional[str]] = mapped_column(nullable=True, type_=Text)
    task_manager_output: Mapped[Optional[str]] = mapped_column(nullable=True, type_=Text)
    state: Mapped[Optional[str]] = mapped_column(nullable=True, type_=Text)
