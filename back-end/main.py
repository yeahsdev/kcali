from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, users, food, dashboard

app = FastAPI(title="KCali API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(food.router)
app.include_router(dashboard.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to KCali API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)