from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fetcher.models import Base
from fetcher.utils import get_database_url

engine = create_engine(get_database_url())
Session = sessionmaker(bind=engine)

def get_session():
    return Session()

def setup_database():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    setup_database()
