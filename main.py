#!/usr/bin/env python3

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app = FastAPI()
app.mount("/public/static", StaticFiles(directory="public/static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.public)
app.include_router(auth.protected)


templates = Jinja2Templates(directory="public/templates")


@app.exception_handler(404)
def page_not_found(request: Request, e):
    return templates.TemplateResponse("404.html", {"request": request})


@app.exception_handler(405)
def action_not_allowed(request: Request, e):
    return templates.TemplateResponse("405.html", {"request": request})


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("404.html", {"request": request})


@app.post("/")
def root(request: Request):
    return templates.TemplateResponse("404.html", {"request": request})
