from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware
from routers import images, users


app = FastAPI()

client = TestClient(app)


origins = 'http://localhost:3000'

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(images.router, tags=['Images'], prefix='/images')
app.include_router(users.router, tags=['Users'], prefix='/users')


@app.get('/')
def root():
    return {'message': 'Hello Ramesh!'}
