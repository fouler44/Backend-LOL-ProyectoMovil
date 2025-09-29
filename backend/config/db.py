# config/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus
from config.config import DB_CONFIG

def _build_url(cfg: dict) -> str:
    user = cfg["user"]
    pwd = quote_plus(cfg["password"])  # por si hay caracteres especiales
    host = cfg["host"]
    port = cfg["port"]
    db   = cfg["dbname"]

    # sslmode es opcional; si usas SSL en producción, cámbialo a 'require'
    sslmode = cfg.get("sslmode", "disable")
    query = f"?sslmode={sslmode}" if sslmode else ""

    return f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}{query}"

DATABASE_URL = _build_url(DB_CONFIG)

engine = create_engine(
    DATABASE_URL,
    echo=True,             # ponlo en False en prod
    future=True,           # API 2.0
    pool_pre_ping=True,    # evita conexiones muertas
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)

Base = declarative_base()

from contextlib import contextmanager
@contextmanager
def get_session():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()
