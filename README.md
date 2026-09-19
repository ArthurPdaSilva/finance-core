# Finance Core

Aplicacao full stack de analise financeira com assistente conversacional baseado em IA. O projeto combina uma API FastAPI com agentes LangGraph, RAG, busca vetorial e consultas SQL, um frontend Next.js e um banco PostgreSQL.

## Arquitetura Docker

```text
Browser :3000 --> frontend (Next.js) --> backend :8000 --> database :5432
                                               |
                                               +--> OpenAI / Langfuse (opcionais)
```

Os servicos pertencem a mesma rede Docker. Por isso, o frontend usa `http://backend:8000` como URL interna da API, enquanto a API fica disponivel no host em `http://localhost:8000`.

| Servico | Imagem | Porta | Funcao |
|---|---|---:|---|
| `database` | `postgres:16-alpine` | 5432 | Persistencia dos dados financeiros e historico de chats |
| `backend` | Dockerfile local | 8000 | API FastAPI e processamento dos agentes |
| `frontend` | Dockerfile local | 3000 | Interface Next.js |

## Execucao com Docker

Requisitos: Docker Engine e Docker Compose.

1. Crie um arquivo `.env` na raiz com pelo menos:

```env
API_KEY=uma-chave-local
OPENAI_API_KEY=sua-chave-openai
```

`LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` e `LANGFUSE_BASE_URL` sao opcionais. Os valores padrao do PostgreSQL funcionam localmente, mas devem ser alterados em ambientes compartilhados.

2. Suba os tres servicos:

```bash
docker compose up --build -d
```

3. Acesse a aplicacao:

- Frontend: http://localhost:3000
- API: http://localhost:8000
- Health check: http://localhost:8000/health

Use o valor de `API_KEY` no formulario inicial. Depois do primeiro acesso, use a opcao de inicializacao do banco para criar as tabelas, inserir os dados de exemplo e montar o vector store. Essa etapa exige `OPENAI_API_KEY` configurada.

Para acompanhar os logs:

```bash
docker compose logs -f backend frontend
```

Para encerrar os containers sem remover os dados:

```bash
docker compose down
```

Para remover tambem o banco persistido:

```bash
docker compose down -v
```

## Execucao local sem Docker

### Backend

```bash
cd backend
uv sync
DATABASE_URL=sqlite:///app.db DATABASE_NAME=app.db uv run --directory src uvicorn main:app --reload
```

### Frontend

Configure `frontend/.env` com:

```env
API_KEY=uma-chave-local
API_URL=http://127.0.0.1:8000
```

Depois execute:

```bash
cd frontend
pnpm install
pnpm dev
```

## Variaveis de ambiente

Os arquivos `backend/.env.example` e `frontend/.env.example` documentam as variaveis de cada servico. Nunca versione chaves de OpenAI, Langfuse ou a chave de acesso da aplicacao.

## Stack

- Python 3.13, FastAPI, SQLAlchemy e PostgreSQL
- LangChain, LangGraph, ChromaDB e Langfuse
- Next.js 16, React 19, TypeScript e Tailwind CSS
- Docker Compose
