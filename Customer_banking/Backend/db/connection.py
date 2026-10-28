from sqlalchemy import (
    create_engine,
    column,
    Integer,
    DateTime,
    String,text)
from sqlalchemy.orm import sessionmaker,declarative_base,Session
from dotenv import load_dotenv
load_dotenv()
import os

DATABASE_URL=os.getenv("DATABASE_URL")

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