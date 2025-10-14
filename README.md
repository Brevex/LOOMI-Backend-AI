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
    * **Modelos:** OpenAI GPT-4 (para o raciocínio do agente) e GPT-3.5-Turbo (para a ferramenta de recomendação).
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
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
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

## 5. CUso de IA no Desenvolvimento

Conforme solicitado no desafio, a IA foi utilizada como uma ferramenta estratégica durante o desenvolvimento.
