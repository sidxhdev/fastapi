import os
import logging

from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool, QueuePool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get database URL from environment variable
DATABASE_URL = os.getenv(
	"DATABASE_URL",
	"postgresql+psycopg://postgres:postgres@localhost:5432/inventory_db",
)

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Use NullPool for RDS (cloud), QueuePool for local development
pool_class = NullPool if ENVIRONMENT == "production" else QueuePool

logger.info(f"Database Environment: {ENVIRONMENT}")
logger.info(f"Connecting to database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'localhost'}")

# Create engine with appropriate pool settings
if ENVIRONMENT == "production":
	engine = create_engine(
		DATABASE_URL,
		poolclass=NullPool,  # No connection pooling for serverless/RDS
		pool_pre_ping=True,
		echo=False,
	)
else:
	engine = create_engine(
		DATABASE_URL,
		pool_pre_ping=True,
		echo=False,
	)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
