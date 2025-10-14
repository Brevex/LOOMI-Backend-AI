from fastapi import FastAPI
from app.api.v1.endpoints import users, auth, paints, chat

app = FastAPI(
    title="Catálogo Inteligente de Tintas com IA",
    description="API para um assistente virtual especialista em tintas Suvinil.",
    version="1.0.0",
)

app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(paints.router, prefix="/api/v1/paints", tags=["Paints"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])


@app.get("/")
def read_root():
    """
    Endpoint raiz que retorna uma mensagem de boas-vindas.
    """
    return {"message": "Bem-vindo ao Catálogo Inteligente de Tintas Suvinil!"}
