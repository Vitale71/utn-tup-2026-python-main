from fastapi import FastAPI
from routers import users, songs

# Create the application instance
app = FastAPI()

# Router to user endpoints
app.include_router(tags=["Users"], router=users.router)
app.include_router(tags=["Songs"], router=songs.router)

# Define a GET route for the root URL
@app.get("/")
def read_root():
    mensaje = "Parte 1 trabajo practico"
    return {"message": mensaje}

''' 
@app.get("/songs")
def read_songs():
    mensaje = "Parte 2 trabajo practico entidad propia canciones"
    return {"message": mensaje}
'''