import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = sa.create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False}
)
SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()