import os
from sqlalchemy import create_engine

#url = f"postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}?sslmode={os.getenv("DB_SSLMODE")}"
url = f"postgresql://postgres:<password>@localhost:5432/testdb?sslmode=disabled"
print(url)
engine = create_engine(url)
conn = engine.connect()
print(conn.execute("SELECT * FROM users"))