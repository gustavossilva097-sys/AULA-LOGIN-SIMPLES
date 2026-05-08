# Criar um sistema SSR

from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session


app = FastAPI(title="SIstema de login simples")

#Roda o codigo:
# python -m uvicorn main:app --reload
