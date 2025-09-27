from dotenv import load_dotenv
import os

load_dotenv()

RIOT_API_KEY = os.getenv("RIOT_API_KEY", "")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "parcial1"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "sslmode": os.getenv("DB_SSLMODE", "disable"),  # opcional
}
