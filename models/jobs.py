from sqlalchemy import String, text
from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str | None] = mapped_column(String(250))
    salary: Mapped[float] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))