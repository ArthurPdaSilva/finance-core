# Finance Core Development Guide

## Visao Geral

Monorepo de uma aplicacao de analise financeira com API FastAPI, agentes LangGraph, RAG, PostgreSQL, frontend Next.js e observabilidade com Langfuse Cloud.

O chat usa a API compativel com OpenAI da OpenRouter. O modelo padrao e gratuito para testes simples; embeddings continuam usando OpenAI para o vector store.

## Estrutura

```text
backend/                  # API FastAPI e processamento de IA
  src/
    config/               # Carregamento central de configuracoes e Langfuse
    db/                   # SQLAlchemy, schema e seeds
    engine/               # Grafo LangGraph, agentes, prompts e tools
    rag/                  # ChromaDB, embeddings e consultas financeiras
    utils/                # LLM e utilitarios

frontend/                 # Aplicacao Next.js e server actions
  src/
    actions/              # Chamadas server-side para a API
    app/                  # Rotas e layouts
    components/           # Componentes de interface
    contexts/             # Estado compartilhado do frontend

docker-compose.yml        # PostgreSQL local da aplicacao
.env.example              # Contrato central de variaveis do ambiente local
```

## Convencoes

- Python: formatacao e lint com Ruff; imports organizados automaticamente.
- TypeScript: seguir as convencoes existentes do Next.js e Biome.
- Variaveis e funcoes de codigo permanecem em ingles; textos da interface podem ser em portugues brasileiro.
- Manter alteracoes pequenas e evitar compatibilidade retroativa sem necessidade concreta.
- Nao versionar bancos, vector stores, builds, dependencias ou segredos.

## Configuracao de Ambiente

- O `.env` da raiz e a fonte central de configuracao local do Docker Compose, backend e frontend executados fora do Docker.
- `.env.example` documenta as variaveis centrais sem valores sensiveis.
- `backend/.env` e `frontend/.env` nao devem ser usados para novas configuracoes; valores locais existentes devem ser migrados para a raiz.
- O Next.js carrega o `.env` raiz quando executado fora do Compose.
- O Compose injeta `API_KEY` e `DOCKER_API_URL` no frontend, mantendo `API_URL` para execucao local no host.
- Em producao, injetar as variaveis a partir de um secret manager, como Vault, AWS Secrets Manager, GCP Secret Manager, Doppler ou Infisical.
- A aplicacao deve ler configuracoes por variaveis de ambiente; nao buscar segredos diretamente em um servico remoto.
- Nunca imprimir o conteudo de arquivos `.env` ou chaves em logs, testes e mensagens de erro.

Variaveis principais:

- `OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL` e `OPENROUTER_MODEL`: chat.
- `OPENAI_API_KEY`: embeddings usados pelo ChromaDB e inicializacao do vector store.
- `DATABASE_URL` e variaveis `POSTGRES_*`: banco financeiro.
- `API_KEY`: autenticacao da API usada pelo frontend.
- `LANGFUSE_HOST`, `LANGFUSE_PUBLIC_KEY` e `LANGFUSE_SECRET_KEY`: Langfuse Cloud.

## Integracoes Docker

- O Compose sobe apenas o PostgreSQL em `localhost:5432`.
- Backend e frontend sao executados no host fora do Compose.
- O backend envia observabilidade para o Langfuse Cloud configurado no ambiente.
- O endpoint `/init-db` inicializa explicitamente as tabelas, seeds e vector store; ele pode resetar dados financeiros e de chat.

## Validacao

Configuracao e integracao:

```bash
docker compose config -q
docker compose up -d database
```

Backend:

```bash
cd backend
uv lock --check
uv run ruff check src
```

Frontend:

```bash
cd frontend
pnpm exec tsc --noEmit
pnpm build
```

## Workflow

1. Ler os arquivos afetados e verificar mudancas locais antes de editar.
2. Alterar apenas os arquivos necessarios.
3. Nunca substituir mudancas feitas pelo usuario ou por outros agentes.
4. Atualizar o `README.md` quando mudar arquitetura, ambiente ou fluxo de desenvolvimento.
5. Rodar as validacoes correspondentes antes de concluir.

## Seguranca

- Chaves fornecidas em conversas ou ambientes compartilhados devem ser rotacionadas se houver risco de exposicao.
- Nao commitar `.env`, tokens, credenciais de banco ou chaves de API.
- Nao executar comandos que imprimam a configuracao resolvida do Compose quando ela contiver segredos.
- Nao usar comandos destrutivos para banco ou Git sem solicitacao explicita.
