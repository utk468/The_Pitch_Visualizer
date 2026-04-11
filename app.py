from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from routers import chat, auth, threads
import uvicorn
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("SERVER STARTUP: Initializing Medical AI", flush=True)
    print("SERVER STARTUP COMPLETE: Ready for requests", flush=True)
    yield

app = FastAPI(title="Medical Triage AI - Optimized", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(threads.router, prefix="/api/threads", tags=["Threads"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])

@app.get("/")
async def root(request: Request):
    """Render the main UI."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

if __name__ == "__main__":
    print("Starting Medical Triage AI Server...")
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
