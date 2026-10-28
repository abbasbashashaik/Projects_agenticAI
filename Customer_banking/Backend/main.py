from db.connection import Base,engine
from models.Accounts import Account
from models.customers import Customer
from models.cards import Card
from models.transaction import Transaction
from models.user import User


Base.metadata.create_all(bind=engine)