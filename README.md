# Finance Core

Aplicacao full stack de analise financeira com assistente conversacional baseado em IA. O projeto combina uma API FastAPI com agentes LangGraph, RAG, busca vetorial e consultas SQL, um frontend Next.js, PostgreSQL e Langfuse Cloud.

## Visao Geral

```text
Browser :3000 --> frontend (Next.js) --> backend :8000 --> database :5432
                                                 |
                                                +--> Langfuse Cloud
                                                |
                                                +--> OpenRouter (chat)
                                                +--> OpenAI (embeddings)
```

O chat usa por padrao `meta-llama/llama-3.3-70b-instruct:free` pela OpenRouter. Esse modelo e adequado para testes simples sem custo de inferencia, sujeito aos limites e disponibilidade da OpenRouter. O vector store usa `text-embedding-3-small` pela OpenAI.

## Estrutura

```text
backend/
  src/config/             configuracao central e Langfuse Cloud
  src/db/                 banco, models e seeds
  src/engine/             grafo, agentes, prompts e tools
  src/rag/                ChromaDB e consultas financeiras
  src/utils/              LLM e utilitarios

frontend/
  src/actions/            server actions
  src/app/                paginas e rotas Next.js
  src/components/         componentes de UI

docker-compose.yml        PostgreSQL, backend e frontend locais
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
| `API_KEY` | Chave administrativa usada somente no `/init-db` |
| `API_URL` | URL do backend quando o frontend roda fora do Docker |
| `DOCKER_API_URL` | URL do backend na rede interna do Compose |
| `OPENROUTER_API_KEY` | Chave do modelo de chat |
| `OPENROUTER_BASE_URL` | URL compativel com a API OpenAI da OpenRouter |
| `OPENROUTER_MODEL` | Modelo usado pelo chat |
| `OPENAI_API_KEY` | Embeddings do ChromaDB e inicializacao do vector store |
| `DATABASE_URL` | URL do banco quando executado fora do Compose |
| `LANGFUSE_HOST` | URL do projeto Langfuse Cloud |
| `LANGFUSE_PUBLIC_KEY` | Chave publica do projeto Langfuse |
| `LANGFUSE_SECRET_KEY` | Chave secreta do projeto Langfuse |

O backend carrega explicitamente o `.env` raiz em `backend/src/config/secrets.py` e nao depende do diretorio atual. Variaveis ja presentes no ambiente, como as injetadas pelo Docker, tem prioridade.

`backend/.env` e `frontend/.env` nao sao mais fontes de configuracao. O Next.js carrega o `.env` raiz durante o desenvolvimento local. No Compose, `API_KEY` e `DOCKER_API_URL` sao injetados no container do frontend.

### Langfuse Cloud

Crie um projeto no [Langfuse Cloud](https://cloud.langfuse.com), copie as chaves de observabilidade e preencha `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` e `LANGFUSE_HOST` no ambiente. O backend envia traces diretamente para o servico Cloud; nenhuma imagem, banco ou fila do Langfuse e executada localmente.

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

3. Suba PostgreSQL, backend e frontend:

```bash
docker compose up --build -d
```

O Compose fornece os servicos locais da aplicacao:

| Servico | Porta | Funcao |
|---|---:|---|
| `database` | 5432 | Dados financeiros e chats |
| `backend` | 8000 | API FastAPI e agentes |
| `frontend` | 3000 | Interface Next.js |

O backend usa PostgreSQL obrigatoriamente e nao possui fallback para SQLite. A inicializacao do banco tambem exige `OPENAI_API_KEY` para criar os embeddings do vector store.

Acesse:

- Frontend: http://localhost:3000
- API: http://localhost:8000
- Health check: http://localhost:8000/health

Para parar sem remover dados:

```bash
docker compose down
```

Para remover tambem os volumes persistidos:

```bash
docker compose down -v
```

## Execucao Local Sem Docker

### Backend

```bash
cd backend
uv sync
uv run --directory src uvicorn main:app --reload
```

O backend encontra o `.env` raiz automaticamente e usa a `DATABASE_URL` PostgreSQL configurada nele. Se o PostgreSQL estiver no Compose, mantenha o banco ativo com `docker compose up -d database` e execute o backend no host.

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
uv run pytest --cov=src --cov-report=term-missing

cd ../frontend
pnpm exec tsc --noEmit
pnpm test
pnpm build
```

## Testes e CI/CD

O backend usa `pytest` com cobertura e o frontend usa Vitest. Os testes nao fazem chamadas reais para OpenRouter, OpenAI ou Langfuse; integracoes externas devem ser mockadas.

Para executar as suites separadamente:

```bash
cd backend
uv run pytest --cov=src --cov-report=term-missing

cd ../frontend
pnpm test
pnpm test:coverage
```

O workflow de Continuous Integration roda em pull requests e pushes para `main`:

- Ruff, lockfile e testes do backend com PostgreSQL de servico;
- Biome, TypeScript, testes Vitest e build do frontend;
- validacao, build e health check do Docker Compose.

Depois que o CI da `main` termina com sucesso, o Continuous Delivery publica no Docker Hub:

- `<DOCKER_USERNAME>/finance-core-backend:latest`;
- `<DOCKER_USERNAME>/finance-core-backend:<commit-sha>`;
- `<DOCKER_USERNAME>/finance-core-frontend:latest`;
- `<DOCKER_USERNAME>/finance-core-frontend:<commit-sha>`.

Configure estes secrets no repositorio GitHub:

| Secret | Uso |
|---|---|
| `DOCKER_USERNAME` | Usuario ou organizacao do Docker Hub |
| `DOCKER_ACCESS_TOKEN` | Access token do Docker Hub com permissao de escrita |

As chaves de OpenRouter, OpenAI, Langfuse e PostgreSQL nao devem ser cadastradas no CI. Elas sao necessarias somente no ambiente de execucao.

## Autenticacao

O acesso da aplicacao usa email, senha e sessoes opacas persistidas no PostgreSQL. O frontend grava apenas o token da sessao em cookie `HttpOnly`; a senha nunca e armazenada em texto puro, sendo protegida com Argon2.

Rotas publicas:

- `/login`: entrada de usuarios existentes;
- `/signup`: criacao de uma nova conta.

Cada chat pertence ao usuario que o criou. Listagens, mensagens, limpeza e operacoes do chat verificam essa propriedade no backend. O `/init-db` continua protegido por `API_KEY` como operacao administrativa e nao participa do login do usuario.

## Seguranca

- Nunca versione `.env`, tokens ou chaves de API.
- Nao imprima o conteudo de arquivos de ambiente ou a configuracao completa resolvida do Compose.
- Nao coloque segredos em variaveis `NEXT_PUBLIC_*` ou no bundle do frontend.
- O endpoint `/init-db` deve ser protegido por `API_KEY` e executado conscientemente, pois recria dados de seed e o vector store.
- As chaves do Langfuse Cloud devem ser tratadas como segredos e nunca expostas no frontend.
- Rotacione chaves que tenham sido expostas em logs, commits ou ambientes compartilhados.

## Stack

- Python 3.13, FastAPI, SQLAlchemy e PostgreSQL
- LangChain, LangGraph, ChromaDB e Langfuse Cloud
- Next.js 16, React 19, TypeScript e Tailwind CSS
- Docker Compose
