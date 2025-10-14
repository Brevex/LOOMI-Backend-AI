import pandas as pd
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from app.db.session import engine
from app.core.config import settings


class ChatService:
    def __init__(self):
        print("Iniciando o ChatService...")
        self.rag_chain = self._build_rag_chain()
        print("ChatService pronto.")

    def _load_paints_from_db(self):
        """Carrega todas as tintas do banco de dados usando pandas."""
        try:
            query = "SELECT * FROM paints"
            df = pd.read_sql(query, engine)
            print(f"Carregadas {len(df)} tintas do banco de dados.")
            return df
        except Exception as e:
            print(f"Erro ao carregar tintas do banco de dados: {e}")
            return pd.DataFrame()

    def _format_docs(self, docs):
        """Formata os documentos recuperados para serem enviados ao prompt."""
        return "\n\n".join(
            f"Nome da Tinta: {doc.metadata.get('name', 'N/A')}\n"
            f"Características: {doc.metadata.get('features', 'N/A')}\n"
            f"Ambiente: {doc.metadata.get('environment', 'N/A')}\n"
            f"Acabamento: {doc.metadata.get('finish_type', 'N/A')}"
            for doc in docs
        )

    def _build_rag_chain(self):
        """Constrói a cadeia de RAG completa."""
        paints_df = self._load_paints_from_db()
        if paints_df.empty:
            return None

        paints_df["document_text"] = paints_df.apply(
            lambda row: f"Nome: {row['name']}. Cor: {row['color']}. "
            f"Características: {row['features']}. "
            f"Ideal para ambientes {row['environment']} "
            f"com acabamento {row['finish_type']}.",
            axis=1,
        )

        documents = paints_df["document_text"].tolist()
        metadatas = paints_df.to_dict("records")
        embeddings = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)
        vector_store = FAISS.from_texts(
            documents, embedding=embeddings, metadatas=metadatas
        )
        retriever = vector_store.as_retriever()

        template = """
            Você é um assistente especialista em tintas da marca Suvinil chamado Suvi.
            Seu objetivo é responder a pergunta do usuário de forma amigável e útil, baseando-se SOMENTE no contexto fornecido abaixo.
            Se a informação não estiver no contexto, diga que não encontrou uma tinta com essas características. Não invente informações.
            Sempre que fizer uma recomendação, justifique com base nas características da tinta.
            Responda em português do Brasil.

            Contexto:
            {context}

            Pergunta: {question}

            Resposta útil:
        """
        prompt = ChatPromptTemplate.from_template(template)

        llm = ChatOpenAI(
            model_name="gpt-5-nano", temperature=0, api_key=settings.OPENAI_API_KEY
        )

        rag_chain = (
            {
                "context": retriever | self._format_docs,
                "question": RunnablePassthrough(),
            }
            | prompt
            | llm
            | StrOutputParser()
        )
        return rag_chain

    def get_ai_response(self, query: str) -> str:
        """
        Recebe uma consulta, invoca a cadeia RAG e retorna a resposta.
        """
        if not self.rag_chain:
            return "Desculpe, o serviço de chat não está disponível devido a um erro de inicialização."

        try:
            return self.rag_chain.invoke(query)
        except Exception as e:
            print(f"Erro ao invocar a cadeia RAG: {e}")
            return "Ocorreu um erro ao processar sua solicitação. Tente novamente."


chat_service_instance = ChatService()
