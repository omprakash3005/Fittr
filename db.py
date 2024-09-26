from sqlmodel import create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()

# DB variables from .env file
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Create MySQL URL
mysql_url = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine
engine = create_engine(mysql_url, echo=True)

# Dependency to get session
def get_session():
    with Session(engine) as session:
        yield session
