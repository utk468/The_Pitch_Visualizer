from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from routers import chat, auth, threads
import uvicorn
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("SERVER STARTUP: Initializing Pitch Visualizer Reasoning Engine", flush=True)
    print("SERVER STARTUP COMPLETE: Ready for storyboard generation", flush=True)
    yield

app = FastAPI(title="The Pitch Visualizer - AI Storyboard Pro", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(threads.router, prefix="/api/threads", tags=["Threads"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])

@app.get("/")
async def root(request: Request):
    """Render the main UI."""
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")

if __name__ == "__main__":
    print("Starting Pitch Visualizer Server...")
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)


