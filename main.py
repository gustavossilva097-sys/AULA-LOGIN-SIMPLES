#Criar um sistema SSR

from fastapi import FastAPI, Depends, Request, Form 
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db, Usuario


app = FastAPI(title="Sistema de login simples")

#Roda o código:
# python -m uvicorn main:app --reload

templates = Jinja2Templates(directory="templetes")

#Rota - método HTTP (get, post)

@app.get("/cadastro")
def tela_cadastro(request:Request):
    return templates.TemplateResponse(
        request,
        "cadastro.html",
        {"request": request}
    )
#Tela de login
@app.get("/login")
def tela_login(request:Request):
    return templates.TemplateResponse(
        request,
        "login.html",
        {"request": request}
    )

#Tela inicial
@app.get("/")
def tela_inicial(request:Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"request": request}
    )

#POST - CRIAR UM USUARIO
@app.post("/cadastro")
def cadastrar_usuario(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    #Procurar o email no banco de dados .

    user_existente = db.query(Usuario).filter_by(email=email).first()
   
    if user_existente:
        return templates.TemplateResponse(
            request,
            "cadastro.html",
            {"request": request, "erro": "Email ja cadastrado."}
        )
    #Cria objeto
    novo_usuario = Usuario(email=email, senha=senha) 
    db.add(novo_usuario)
    db.commit()

    return RedirectResponse(url="/login", status_code=303)

#Rota fazer login
@app.post("/login")
def fazer_login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    
    #Verificar login
    usuario = db.query(Usuario).filter(Usuario.email == email).filter(Usuario.senha == senha).first()
    
    if usuario is None:
        return templates.TemplateResponse(
            request,
            "login.html",
            {"request": request, "erro": "Email ou senha inválidos"}
        )
    
    response = RedirectResponse(url="/poslogin", status_code=303)

    #Criando o cookie simples
    response.set_cookie(

        key="usuario_id",
        value=str(usuario.id)

    )

    return response

#Tela protegida

@app.get("/poslogin")
def tela_poslogin(request: Request, db: Session = Depends(get_db)):

    #Verificar id no cookie
    usuario_id = request.cookies.get("usuario_id")

    if usuario_id is None:
        return RedirectResponse(url="/login", status_code=303)

    user_existente = db.query(Usuario).get(int(usuario_id))

    return templates.TemplateResponse(
        request,
        "inicio.html",
        {"request": request, "usuario": user_existente}
    )    

# Logout do sistema - sair
@app.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("usuario_id")
    return response
