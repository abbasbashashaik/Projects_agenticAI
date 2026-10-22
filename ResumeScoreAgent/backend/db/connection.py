from sqlalchemy import (
    create_engine,
    column,
    Integer,
    DateTime,
    String,text)
from sqlalchemy.orm import sessionmaker,declarative_base,Session

DATABASE_URL="postgresql://postgres:system@localhost:5432/auth_database"

engine=create_engine(DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()
# with engine.connect() as con:
#     r=con.execute(text("select 1"))
#     if r.fetchone():
#         print("success")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

