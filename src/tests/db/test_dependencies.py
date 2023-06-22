from .test_database import TestingSessionLocal, test_engine

# Dependency
def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()