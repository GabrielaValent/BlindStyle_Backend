from fastapi import FastAPI, HTTPException
from app.api.v1.routes.items import router as items_router
from app.api.v1.routes.users import router as users_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular dev server URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(items_router, prefix="/api/v1/items", tags=["items"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to BlindStyle, the Clothing API"}
