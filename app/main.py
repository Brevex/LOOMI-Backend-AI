from fastapi import FastAPI
from app.api.v1.endpoints import users

app = FastAPI(
    title="Catálogo Inteligente de Tintas com IA",
    description="API para um assistente virtual especialista em tintas Suvinil.",
    version="1.0.0",
)

app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])


@app.get("/")
def read_root():
    """
    Endpoint raiz que retorna uma mensagem de boas-vindas.
    """
    return {"message": "Bem-vindo ao Catálogo Inteligente de Tintas Suvinil!"}
