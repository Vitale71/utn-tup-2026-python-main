from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str
"""[cite: 1]

`table=True`: Le indica a SQLModel que esta clase no es solo un esquema de validación, sino que representa una "tabla real en la base de datos" (en la BD la tabla se llamará `hero`)[cite: 1, 2].
`id: int | None`: Es la clave primaria (`primary_key=True`)[cite: 1]. Es opcional (`None`) porque al momento de crear un nuevo héroe en Python todavía no tiene ID; la base de datos se lo asigna automáticamente al guardarlo.
`index=True`: Crea un índice en la base de datos para las columnas `name` y `age`[cite: 1]. Esto optimiza la velocidad de las búsquedas por nombre o edad[cite: 2].

"""

### 2. Configuración de la Base de Datos

#python
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)
"""[cite: 1]

`sqlite_url`: Especifica que se utilizará una base de datos local SQLite llamada `database.db`[cite: 1].
`create_engine`: Es el motor de conexión de SQLAlchemy/SQLModel[cite: 1].
`{"check_same_thread": False}`: Se requiere específicamente en SQLite con FastAPI porque FastAPI procesa solicitudes en múltiples hilos (threads) paralelos[cite: 1].

"""

### 3. Creación de Tablas e Inyección de Dependencias (Sessions)

#python
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
"""[cite: 1]

`create_db_and_tables()`: Lee todas las clases que hereden de `SQLModel` con `table=True` y crea las tablas e índices en SQLite si no existen[cite: 1, 2].
`get_session()`: Es una función generadora con `yield`[cite: 1]. Abre una sesión de base de datos para cada petición HTTP y la cierra automáticamente al terminar la solicitud[cite: 1].
`SessionDep`: Es un tipo personalizado de FastAPI usando `Annotated` y `Depends`[cite: 1]. Esto permite pedir la sesión en cualquier endpoint escribiendo simplemente `session: SessionDep` de forma limpia[cite: 1].

"""

### 4. Inicialización de FastAPI y Eventos de Arranque

#python
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
"""[cite: 1]

`@app.on_event("startup")`: Ejecuta la función `create_db_and_tables()` automáticamente al iniciar el servidor de FastAPI[cite: 1], 
asegurando que la base de datos y sus tablas existan antes de recibir peticiones[cite: 1, 2].

"""

### 5. Rutas / Endpoints (Operaciones CRUD)

#### A) Crear un Héroe (POST)
#python
@app.post("/heroes/")
def create_hero(hero: Hero, session: SessionDep) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero
"""[cite: 1]
1. Recibe en el cuerpo de la petición un objeto JSON que valida contra la clase `Hero`[cite: 1].
2. `session.add(hero)` coloca el héroe en la sesión actual[cite: 1].
3. `session.commit()` guarda los cambios permanentemente en la base de datos[cite: 1].
4. `session.refresh(hero)` vuelve a cargar los datos desde la BD para obtener el `id` autogenerado[cite: 1].

"""

#### B) Consultar Lista de Héroes con Paginación (GET)
#python
@app.get("/heroes/")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes
"""[cite: 1]
 Permite paginar los resultados usando los parámetros de búsqueda `offset` (saltar N registros) y `limit` (máximo a traer, con un límite máximo estricto de 100 usando `Query(le=100)`)[cite: 1].
 Executa una consulta SQL: `SELECT * FROM hero LIMIT ... OFFSET ...`[cite: 1, 2].

"""

#### C) Leer un Héroe por ID (GET)
#python
@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero
"""[cite: 1]
Utiliza `session.get(Hero, hero_id)` para buscar directamente por la clave primaria[cite: 1].
Si no existe, devuelve un error HTTP 404[cite: 1].

"""

#### **D) Eliminar un Héroe (DELETE)**
#python
@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
"""[cite: 1]
 Busca el registro; si existe, lo elimina con `session.delete(hero)` y confirma la transacción con `session.commit()`[cite: 1].

"""

### El archivo `database.db`
"""
El archivo adjunto `database.db` es el archivo binario generado por SQLite tras haber ejecutado este script[cite: 2]. 
En la estructura de ese archivo se puede observar que creó exactamente la tabla `hero` y los dos índices (`ix_hero_name` e `ix_hero_age`)
definidos en la clase Python[cite: 1, 2].

---

¿Hay alguna sección específica de este código (como la inyección de dependencias `Annotated`, las sesiones o las consultas con `select`)
que quieras profundizar antes de pasar a la siguiente carpeta?
"""