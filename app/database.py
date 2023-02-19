from click import echo
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.create_db import Base
from .models import UserTable


# engine=create_engine("postgresql://{YOUR_DATABASE_USER}:{YOUR_DATABASE_PASSWORD}@localhost/{YOUR_DATABASE_NAME}",
#     echo=True
# )
SQLALCHEMY_DATABASE_URL = "sqlite:///./circle.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)


Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
