from sqlalchemy.orm import sessionmaker

from db.postgres import engine

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
