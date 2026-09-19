# Finance Core

Aplicacao full stack de analise financeira com assistente conversacional baseado em IA. O projeto combina uma API FastAPI com agentes LangGraph, RAG, busca vetorial e consultas SQL, um frontend Next.js, PostgreSQL e Langfuse self-hosted.

## Visao Geral

```text
Browser :3000 --> frontend (Next.js) --> backend :8000 --> database :5432
                                                |
                                                +--> Langfuse :3000 --> ClickHouse / Redis / MinIO
                                                |
                                                +--> OpenRouter (chat)
                                                +--> OpenAI (embeddings)
```

O chat usa por padrao `meta-llama/llama-3.3-70b-instruct:free` pela OpenRouter. Esse modelo e adequado para testes simples sem custo de inferencia, sujeito aos limites e disponibilidade da OpenRouter. O vector store usa `text-embedding-3-small` pela OpenAI.

## Estrutura

```text
backend/
  src/config/             configuracao central e Langfuse
  src/db/                 banco, models e seeds
  src/engine/             grafo, agentes, prompts e tools
  src/rag/                ChromaDB e consultas financeiras
  src/utils/              LLM e utilitarios

frontend/
  src/actions/            server actions
  src/app/                paginas e rotas Next.js
  src/components/         componentes de UI

docker-compose.yml        stack local completa
.env.example              contrato central de variaveis
```

## Configuracao Centralizada

### Desenvolvimento local

O `.env` da raiz e a fonte central para o Docker Compose e para o backend executado localmente. Comece pelo exemplo:

```bash
cp .env.example .env
```

Preencha os valores sensiveis no `.env` local. Nunca coloque chaves reais no `.env.example`.

Variaveis principais:

| Variavel | Uso |
|---|---|
| `API_KEY` | Chave da aplicacao usada nas chamadas do frontend para o backend |
| `API_URL` | URL do backend quando o frontend roda fora do Docker |
| `DOCKER_API_URL` | URL do backend na rede interna do Compose |
| `OPENROUTER_API_KEY` | Chave do modelo de chat |
| `OPENROUTER_BASE_URL` | URL compativel com a API OpenAI da OpenRouter |
| `OPENROUTER_MODEL` | Modelo usado pelo chat |
| `OPENAI_API_KEY` | Embeddings do ChromaDB e inicializacao do vector store |
| `DATABASE_URL` | URL do banco quando executado fora do Compose |
| `LANGFUSE_*` | Banco, chaves e URL do Langfuse |

O backend carrega explicitamente o `.env` raiz em `backend/src/config/secrets.py` e nao depende do diretorio atual. Variaveis ja presentes no ambiente, como as injetadas pelo Docker, tem prioridade.

`backend/.env` e `frontend/.env` nao sao mais fontes de configuracao. O Next.js carrega o `.env` raiz durante o desenvolvimento local. No Compose, `API_KEY` e `DOCKER_API_URL` sao injetados no container do frontend.

### Producao

Nao copie `.env` para imagens nem versiona segredos. Use um secret manager, como Vault, AWS Secrets Manager, GCP Secret Manager, Doppler ou Infisical, e injete as variaveis no processo do backend e nos demais servicos.

Configuracoes nao sensiveis tambem podem vir de um servico central de configuracao quando houver necessidade de alteracao dinamica. Para este projeto, variaveis de ambiente injetadas pelo deploy sao suficientes.

## Docker Compose

Requisitos: Docker Engine e Docker Compose.

1. Configure o `.env` raiz.
2. Valide a sintaxe sem imprimir os valores resolvidos:

```bash
docker compose config -q
```

3. Suba a stack:

```bash
docker compose up --build -d
```

Servicos principais:

| Servico | Porta | Funcao |
|---|---:|---|
| `frontend` | 3000 | Interface Next.js |
| `backend` | 8000 | API FastAPI e agentes |
| `database` | 5432 | Dados financeiros e chats |
| `langfuse-web` | 3001 | Dashboard de observabilidade |

Acesse:

- Frontend: http://localhost:3000
- API: http://localhost:8000
- Health check: http://localhost:8000/health
- Langfuse: http://localhost:3001

Depois do primeiro acesso, use a inicializacao do banco para criar tabelas, inserir seeds e montar o vector store. Essa etapa exige `OPENAI_API_KEY`, pois embeddings da OpenRouter nao fazem parte deste fluxo.

Para acompanhar logs:

```bash
docker compose logs -f backend frontend
```

Para parar sem remover dados:

```bash
docker compose down
```

Para remover tambem os volumes persistidos:

```bash
docker compose down -v
```

## Execucao Sem Docker

### Backend

```bash
cd backend
uv sync
uv run --directory src uvicorn main:app --reload
```

O backend encontra o `.env` raiz automaticamente. Se quiser usar SQLite local, defina `DATABASE_URL=sqlite:///app.db` e `DATABASE_NAME=app.db` no ambiente do processo.

### Frontend

Execute:

```bash
cd frontend
pnpm install
pnpm dev
```

## Qualidade

Antes de abrir uma alteracao:

```bash
docker compose config -q

cd backend
uv lock --check
uv run ruff check src

cd ../frontend
pnpm exec tsc --noEmit
pnpm build
```

## Seguranca

- Nunca versione `.env`, tokens ou chaves de API.
- Nao imprima o conteudo de arquivos de ambiente ou a configuracao completa resolvida do Compose.
- Nao coloque segredos em variaveis `NEXT_PUBLIC_*` ou no bundle do frontend.
- O endpoint `/init-db` deve ser protegido por `API_KEY` e executado conscientemente, pois recria dados de seed e o vector store.
- Rotacione chaves que tenham sido expostas em logs, commits ou ambientes compartilhados.

## Stack

- Python 3.13, FastAPI, SQLAlchemy e PostgreSQL
- LangChain, LangGraph, ChromaDB e Langfuse
- Next.js 16, React 19, TypeScript e Tailwind CSS
- Docker Compose
