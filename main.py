from db import engine, Base
import models  # asegura que se importen/rexporten todas las clases vía __init__.py

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("✅ Esquema listo")
