from fastapi import FastAPI, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.future import select
from sqlalchemy.sql import text
from pydantic import BaseModel
from datetime import datetime
from database import get_db
from models import Tarea

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de tarea
class TareaEditada(BaseModel):
    titulo: str = None
    descripcion: str = None
    responsable: str = None
    estado: str = None

    class Config:
        orm_mode = True

# Crear una nueva tarea
@app.post('/tareas/', tags=['ProyectoWWW'])
async def create_tarea(
        titulo: str = Body(),
        descripcion: str = Body(),
        responsable: str = Body(),
        db: AsyncSession = Depends(get_db)
    ):

    fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fecha_modificacion = fecha_creacion

    new_tarea = Tarea(
        titulo=titulo,
        descripcion=descripcion,
        responsable=responsable,
        fecha_creacion=fecha_creacion,
        fecha_modificacion=fecha_modificacion
    )

    db.add(new_tarea)
    await db.commit()
    await db.refresh(new_tarea)

    query_all = select(Tarea)
    result = await db.execute(query_all)
    tareas = result.scalars().all()

    return tareas

# Obtener todas las tareas
@app.get('/tareas/', tags=['ProyectoWWW'])
async def read_tareas(db: AsyncSession = Depends(get_db)):
    query_all = select(Tarea)
    restul = await db.execute(query_all)
    tareas = restul.scalars().all()
    return tareas

# Editar una tarea
@app.put('/tareas/{id}', tags=['ProyectoWWW'])
async def edit_tarea(
    id: int,
    tarea_editada: TareaEditada,
    db: AsyncSession = Depends(get_db)):

    # Consulta para obtener la tarea
    query = select(Tarea).filter(Tarea.id == id)
    result = await db.execute(query)
    tarea = result.scalar_one_or_none()

    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    fecha_modificacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Actualizar los campos de la tarea con los datos recibidos
    if tarea_editada.titulo is not None:
        tarea.titulo = tarea_editada.titulo
    if tarea_editada.descripcion is not None:
        tarea.descripcion = tarea_editada.descripcion
    if tarea_editada.responsable is not None:
        tarea.responsable = tarea_editada.responsable
    if tarea_editada.estado is not None:
        tarea.estado = tarea_editada.estado
    tarea.fecha_modificacion = fecha_modificacion

    # Guardar los cambios en la base de datos
    db.add(tarea)
    await db.commit()

    query_all = select(Tarea)
    result = await db.execute(query_all)
    tareas = result.scalars().all()

    return tareas

# Eliminar una tarea
@app.delete('/tareas/{id}', tags=['ProyectoWWW'])
async def delete_tarea(id: int, db: AsyncSession = Depends(get_db)):
    # Consulta para obtener la tarea
    query = select(Tarea).filter(Tarea.id == id)
    result = await db.execute(query)
    tarea = result.scalar_one_or_none()

    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    # Eliminar la tarea de la base de datos
    await db.delete(tarea)
    await db.commit()

    # Consultar las tareas actualizadas
    query_all = select(Tarea)
    restul_all = await db.execute(query_all)
    tareas_actualizadas = restul_all.scalars().all()

    return tareas_actualizadas