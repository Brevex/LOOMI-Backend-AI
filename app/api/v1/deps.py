from collections.abc import Generator
from app.db.session import SessionLocal


def get_db() -> Generator:
    """
    Função geradora para injeção de dependência da sessão do banco de dados.
    Garante que a sessão seja sempre fechada após a requisição.
    """
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db:
            db.close()
