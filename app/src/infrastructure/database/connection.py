from sqlalchemy import create_engine, Engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator
import os
import time
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logger = logging.getLogger(__name__)

# Base class for all models - SINGLE SOURCE OF TRUTH
Base = declarative_base()


def get_connection_url() -> str:
    """
    Build database connection URL from environment variables or default values.
    
    Returns:
        str: Database connection URL
    """
    db_user = os.getenv("DB_USER", "carsales_user")
    db_password = os.getenv("DB_PASSWORD", "Mudar123!")
    db_host = os.getenv("DB_HOST", "db-carsales")
    db_port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME", "carsales")
    
    # Build MySQL connection URL
    connection_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    logger.info(f"Database connection URL: mysql+pymysql://{db_user}:***@{db_host}:{db_port}/{db_name}")
    return connection_url


def get_engine() -> Engine:
    """
    Create and return a SQLAlchemy engine instance with retry logic.
    
    Returns:
        Engine: SQLAlchemy engine instance
    """
    connection_url = get_connection_url()
    
    # Retry connection logic for containerized environments
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting database connection (attempt {attempt + 1}/{max_retries})")
            
            engine = create_engine(
                connection_url,
                echo=os.getenv("SQL_ECHO", "False").lower() == "true",
                pool_pre_ping=True,
                pool_recycle=300,
                pool_size=5,
                max_overflow=10
            )
            
            # Test connection
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            
            logger.info("✅ Database connection established successfully")
            return engine
            
        except Exception as e:
            logger.warning(f"❌ Database connection attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error("❌ All database connection attempts failed")
                raise e


# Global engine instance
engine = get_engine()

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.
    
    Yields:
        Session: Database session
        
    Raises:
        Exception: If there's an error with the database session
    """
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        session.rollback()
        logger.error(f"Database session error: {str(e)}")
        raise e
    finally:
        session.close()


def create_tables():
    """
    Create all database tables based on the models.
    """
    try:
        # Import all models to ensure they are registered with Base
        from src.infrastructure.database.models import (
            UserModel, MotorVehicleModel, CarModel, MotorcycleModel,
            ClientModel, SaleModel, MessageModel
            # EmployeeModel,  # TODO: Implementar quando necessário
        )
        
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Error creating database tables: {str(e)}")
        raise e


def drop_tables():
    """
    Drop all database tables.
    
    ⚠️  WARNING: This will delete all data!
    """
    try:
        logger.warning("Dropping all database tables...")
        Base.metadata.drop_all(bind=engine)
        logger.warning("⚠️  All database tables dropped")
    except Exception as e:
        logger.error(f"❌ Error dropping database tables: {str(e)}")
        raise e
