from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Se carga las variables de entorno
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Verifica que se cargo la variable de entorno
if not DATABASE_URL:
    raise ValueError("DATABASE_URL no esta definida")

# Motor con la base datos
engine = create_async_engine(DATABASE_URL, echo=True)

# Fabrica de sesiones
async_sesion = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Obtener la sesion de la base de datos
async def get_db():
    async with async_sesion() as sesion:
        yield sesion