import pandas as pd
import re
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from openai import OpenAI

from app.db.session import engine
from app.core.config import settings


def _format_docs(docs):
    """Formata os documentos recuperados para serem enviados ao prompt."""
    return "\n\n".join(
        f"Nome da Tinta: {doc.metadata.get('name', 'N/A')}\n"
        f"Cor: {doc.metadata.get('color', 'N/A')}\n"
        f"Características: {doc.metadata.get('features', 'N/A')}\n"
        f"Ambiente: {doc.metadata.get('environment', 'N/A')}\n"
        f"Acabamento: {doc.metadata.get('finish_type', 'N/A')}"
        for doc in docs
    )


def _generate_image(description: str) -> str:
    """
    Gera uma imagem usando DALL-E 3 com base em uma descrição.
    Retorna uma string contendo a URL da imagem gerada.
    """
    try:
        print(f"Gerando imagem com a descrição: {description}")
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"Uma foto realista de alta qualidade de: {description}. Sem texto ou logos na imagem.",
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        print(f"URL da imagem gerada: {image_url}")
        return f"Aqui está uma simulação visual para você: {image_url}"
    except Exception as e:
        print(f"Erro ao gerar imagem com DALL-E: {e}")
        return "Não foi possível gerar a imagem."


class ChatService:
    def __init__(self):
        print("Iniciando o ChatService com Agente...")
        self.agent_executor = self._build_agent()
        print("ChatService pronto.")

    def _build_rag_chain(self):
        """Constrói a cadeia RAG que será usada como uma ferramenta."""
        paints_df = pd.read_sql("SELECT * FROM paints", engine)
        if paints_df.empty:
            return None

        paints_df["document_text"] = paints_df.apply(
            lambda row: f"Nome: {row['name']}. Características: {row['features']}. "
            f"Ambiente: {row['environment']}. Acabamento: {row['finish_type']}.",
            axis=1,
        )

        vector_store = FAISS.from_texts(
            paints_df["document_text"].tolist(),
            embedding=OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY),
            metadatas=paints_df.to_dict("records"),
        )
        retriever = vector_store.as_retriever()

        template = """
            Você é um especialista em tintas Suvinil. Responda à pergunta do usuário baseando-se SOMENTE no contexto fornecido.
            Seja amigável e recomende a melhor tinta.
            Contexto: {context}
            Pergunta: {question}
            Resposta:
        """
        prompt = ChatPromptTemplate.from_template(template)
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo", temperature=0, api_key=settings.OPENAI_API_KEY
        )

        return {
            "context": retriever | _format_docs,
            "question": RunnablePassthrough(),
        } | prompt

    def _build_agent(self):
        """Constrói o Agente Orquestrador com as ferramentas."""
        rag_chain = self._build_rag_chain()
        if not rag_chain:
            return None

        tools = [
            Tool(
                name="RecomendadorDeTintas",
                func=rag_chain.invoke,
                description="""Use esta ferramenta para responder perguntas sobre tintas,
                recomendar produtos ou encontrar a melhor tinta para uma situação específica.
                Esta deve ser sempre sua primeira escolha.""",
            ),
            Tool(
                name="GeradorDeImagemDeAmbiente",
                func=_generate_image,
                description="""Use esta ferramenta APENAS se o usuário pedir explicitamente para
                ver uma simulação visual, como 'mostre como ficaria' ou 'gere uma imagem'.
                O input para esta ferramenta deve ser uma descrição detalhada do ambiente
                e da cor da tinta recomendada pela outra ferramenta.""",
            ),
        ]

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Você é Suvi, um assistente especialista em tintas Suvinil.
            Seu objetivo é ajudar os usuários a escolher a tinta perfeita.
            1. Sempre use a ferramenta 'RecomendadorDeTintas' PRIMEIRO para encontrar a tinta ideal.
            2. Se o usuário pedir para ver como ficaria, use a ferramenta 'GeradorDeImagemDeAmbiente' DEPOIS.
            3. Sua resposta final deve ser amigável e combinar o texto da recomendação com a URL da imagem, se ela foi gerada.""",
                ),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        llm = ChatOpenAI(model="gpt-4", temperature=0, api_key=settings.OPENAI_API_KEY)
        agent = create_openai_tools_agent(llm, tools, prompt)
        return AgentExecutor(agent=agent, tools=tools, verbose=True)

    def get_ai_response(self, query: str) -> dict:
        """
        Recebe uma consulta, invoca o agente e retorna um dicionário com a resposta e a URL da imagem.
        """
        if not self.agent_executor:
            return {"answer": "Serviço de IA indisponível.", "image_url": None}

        try:
            response = self.agent_executor.invoke({"input": query})
            output_text = response.get(
                "output", "Não consegui processar sua solicitação."
            )

            image_url = None
            match = re.search(r"https?://[^\s)]+", output_text)
            if match:
                image_url = match.group(0)

            return {"answer": output_text, "image_url": image_url}
        except Exception as e:
            print(f"Erro ao invocar o agente: {e}")
            return {
                "answer": "Ocorreu um erro ao processar sua solicitação.",
                "image_url": None,
            }


chat_service_instance = ChatService()
