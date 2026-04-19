from fastapi import FastAPI
from .database import Base, engine
from .routes import auth, tasks
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)



app = FastAPI()

origins = [
    "http://localhost:8000",    # Vue/other dev port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # List of allowed origins
    allow_credentials=True,           # Allow cookies and authentication headers
    allow_methods=["*"],              # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # Allow all request headers
)

app.include_router(auth.router)
app.include_router(tasks.router)