import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post,user,auth,vote
from .config import settings
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


models.Base.metadata.create_all(bind=engine)

app = FastAPI() #Create instance of fastAPI

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Serve static files (like styles.css) from the 'static' directory
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# Method used: GET and / defines url -All Methods[https://www.geeksforgeeks.org/different-kinds-of-http-requests/] where @ represents decorator 
@app.get("/")
async def root():
    file_path = os.path.join(os.path.dirname(__file__), "documentation.html")
    with open(file_path, "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)


# @app.get('/sqlalchemy')
# def test_posts(db: Session = Depends(get_db)): #getDB creates session everytime and generate sessions to it.
#    posts= db.query(models.Post).all() #from models file access Post
#    return{"Status:":posts}


