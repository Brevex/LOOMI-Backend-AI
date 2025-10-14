# LOOMI-Backend-AI

# Catálogo Inteligente de Tintas com IA

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Powered-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT%20%26%20DALL--E%203-green.svg)

## 1. Introdução

Este projeto é um **Assistente Inteligente** que atua como um especialista virtual em tintas da marca Suvinil. O objetivo é ajudar usuários a escolherem o produto ideal com base em suas necessidades e preferências, respondendo a perguntas em linguagem natural e até mesmo gerando simulações visuais da tinta aplicada em um ambiente.

A solução foi desenvolvida como parte do Desafio Back-end IA da Loomi.

## 2. Funcionalidades Principais

* **API RESTful Completa:** Gerenciamento de usuários e do catálogo de tintas.
* **Autenticação Segura:** Sistema de login com autenticação baseada em tokens JWT.
* **Assistente de IA (RAG):** Um chatbot que utiliza **Retrieval-Augmented Generation (RAG)** para buscar informações em um banco de dados PostgreSQL e fornecer recomendações precisas e contextuais.
* **Geração Visual com DALL·E 3:** Um recurso opcional onde o assistente pode gerar uma imagem realista de um ambiente com a cor e o tipo de tinta recomendados, caso o usuário solicite.
* **Documentação Interativa:** Geração automática de documentação da API com Swagger UI e ReDoc, fornecida pelo FastAPI.

## 3. Tecnologias Utilizadas

O projeto foi construído seguindo os princípios de **Clean Architecture** e **SOLID** para garantir modularidade, testabilidade e manutenibilidade.

* **Linguagem:** Python
* **Framework Back-end:** FastAPI
* **Banco de Dados:** PostgreSQL
* **IA & LangChain:**
    * **Orquestração:** Agente com Ferramentas (`AgentExecutor`).
    * **Modelos:** OpenAI GPT-5-nano.
    * **Geração de Imagem:** OpenAI DALL·E 3.
    * **Busca de Dados (RAG):** Embeddings da OpenAI com o banco de dados vetorial em memória FAISS.
* **Containerização:** Docker e Docker Compose para um ambiente de desenvolvimento e produção consistente.

## 4. Como Executar o Projeto

Com Docker e Docker Compose instalados, você pode subir toda a aplicação com um único comando principal.

### Pré-requisitos

* Docker
* Docker Compose

### Passo a Passo

**1. Clone o Repositório**
```bash
git clone https://github.com/Brevex/LOOMI-Backend-AI.git
cd LOOMI-Backend-AI
```

**2. Configure o Ambiente**
```bash
# Copie o arquivo de exemplo
cp .env.example .env
```

**3. Suba a Aplicação**
```bash
docker compose up --build -d
```

**4. Inicialize o Banco de Dados**
```bash
# 1. Criar as tabelas 'users' e 'paints'
docker compose exec api python scripts/create_tables.py

# 2. Popular a tabela 'paints' com os dados do arquivo CSV
docker compose exec api python scripts/load_data.py
```

**5. Acesse a API!**
A aplicação está 100% funcional. Você pode acessar a documentação interativa no seu navegador:

http://localhost:8000/docs

## 5. Uso de IA no Desenvolvimento

Conforme solicitado no desafio, a IA foi utilizada como uma ferramenta estratégica durante o desenvolvimento.

* **Ferramenta Principal:** Gemini (Google)
* **Como foi Usada:** O Gemini atuou como um assistente de programação (pair programmer), ajudando a acelerar o desenvolvimento, depurar erros e refinar a arquitetura.
* **Motivo da Escolha:** O Gemini, dentre os modelos de LLM, tem como diferencial sua enorme janela de contexto que favorece respostas coesas e favoráveis a tarefas extensas (como programação)

### Exemplos de Prompts Utilizados


* **Escolha da Stack:** "Irei desenvolver um chatbot para recomendação de tintas da marca Suvinil e suas posíveis aplicações. A linguagem adotada será o python 3.13. O banco de dados utilizado será o PostgreSQL. O LLM utilizado será o chatGPT da OpenAi. Utilizaremos RAG para buscar informações em um banco de dados PostgreSQL e fornecer recomendações precisas e contextuais. Seu trabalho será me fornecer uma lista de prós e contras da utilização dos frameworks Django, FastAPI e Flask Para a implementação do backend deste projeto."
* **Sugestões de melhorias:** "Essa implementação provisória faz múltiplas consultas SQL para cada pergunta. Utilize o RAG + agente para fazer as buscas relevantes localmente através do banco de dados vetorial. Aplique um regex para reconhecer um padrão universal de URL ao invés de um texto fixo e sucetível a falhas"
* **Geração de scripts auxiliares:** "Utilize a biblioteca pandas e sqlalchemy para realizar a leitura de um arquivo CSV e carregar os dados lidos para um banco de dados. Os dados do CSV devem ser organizados em um dataframe. Faça a leitura do banco de dados para garantir que duplicatas não sejam exportadas e devidamente ignoradas. Crie um objeto do tipo Paint e o adicione à sessão do banco de dados."
* **Criação de Testes:** "Crie um script que simula o processo de criação e leitura de usuários e tintas diretamente no banco de dados para garantir que as funções crud e security operem como o esperado. O script deverá criar e salvar usuários no banco. Use assert para confirmar se os dados do usuário criado no banco são idênticos aos dados de entrada. Se uma verificação assert falhar, o script para imediatamente deve acusar um erro, indicando que o teste falhou. Verifique se o hash foi aplicado na senha antes de salvar no banco de dados e garantir que a senha original corresponde ao hash salvo. No final, o script removerá os dados inseridos no banco."
* **Depuração de erros:** Aqui utilizei prompts variados para sugerir correções a erros de execução que envolviam conflitos
