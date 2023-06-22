from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_PATH = "./metadata-test.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)