
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post,user,auth,vote
from .config import settings


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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# Method used: GET and / defines url -All Methods[https://www.geeksforgeeks.org/different-kinds-of-http-requests/] where @ represents decorator 
@app.get("/")
async def root(): #Defining function//root is a function name

    return {"Yello":"Successfull"}

# @app.get('/sqlalchemy')
# def test_posts(db: Session = Depends(get_db)): #getDB creates session everytime and generate sessions to it.
#    posts= db.query(models.Post).all() #from models file access Post
#    return{"Status:":posts}


