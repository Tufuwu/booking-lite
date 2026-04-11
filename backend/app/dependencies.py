from sqlalchemy.orm import sessionmaker

def get_db():
    db = sessionmaker()
    try:
        yield db
    finally:
        db.close()