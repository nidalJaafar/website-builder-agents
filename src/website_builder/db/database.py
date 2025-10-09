import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base

db = sa.create_engine("sqlite:///test.db")
Db_session = sessionmaker(bind=db)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(db)