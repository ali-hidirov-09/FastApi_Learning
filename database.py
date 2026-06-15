from sqlalchemy import create_engine

sqlite_url = "sqlite:///./learn.db"

engine = create_engine(sqlite_url, echo=True)
