from fastapi import FastAPI

app = FastAPI(
    title="Catálogo Inteligente de Tintas com IA",
    description="API para um assistente virtual especialista em tintas Suvinil.",
    version="1.0.0",
)


@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Catálogo Inteligente de Tintas Suvinil!"}
