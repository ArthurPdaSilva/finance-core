
**Overview**
- **Repo:** Este repositório é o core que contém dois projetos independentes: o backend (API em Python/FastAPI) e o frontend (aplicação Next.js). Use as instruções abaixo para executar cada um separadamente em desenvolvimento.

**Prerequisites**
- **Python:** instale Python >= 3.13 para o backend.
- **Node / pnpm:** instale Node.js (compatível com Next 16) e `pnpm` para o frontend (o projeto usa `pnpm` no lockfile).

**Backend (API)**
- **Localização:** [backend/src/main.py](backend/src/main.py#L1-L80)
- **Instalar dependências:**
	- Crie e ative um virtualenv:
		`python -m venv .venv` (Windows: `.\.venv\Scripts\Activate.ps1` ou `.\.venv\Scripts\activate`)
	- Atualize pip e instale o pacote do projeto a partir do `pyproject.toml`:
		`python -m pip install --upgrade pip` then `python -m pip install -e ./backend`
- **Variáveis de ambiente:** copie ou crie um arquivo `.env` dentro de `backend/` com pelo menos:
	- `OPENAI_API_KEY` — sua chave OpenAI
	- `API_KEY` — chave para usar o endpoint `/init-db` e proteger a API
	- `DATABASE_URL` — (ex.: `sqlite:///app.db`)
	Veja o arquivo de exemplo em [backend/.env.example](backend/.env.example) para referência — copie para `backend/.env` e preencha os valores (não comitar chaves reais).
- **Rodar em desenvolvimento:**
	- Entre na pasta `backend/src` e execute o Uvicorn:
		`uvicorn main:app --reload --host 127.0.0.1 --port 8000`
	- A API ficará disponível em `http://127.0.0.1:8000` (ou `http://localhost:8000`).

**Frontend (Next.js)**
- **Localização:** [frontend/package.json](frontend/package.json#L1-L40)
- **Instalar dependências:**
	- No diretório `frontend`, execute:
		`pnpm install`
- **Variáveis de ambiente:** crie `frontend/.env` com pelo menos:
	- `API_KEY` — mesma chave usada pelo backend para chamadas autenticadas
	- `API_URL` — URL da API (ex.: `http://127.0.0.1:8000`)
	Veja [frontend/.env.example](frontend/.env.example) como referência — copie para `frontend/.env` e preencha os valores.
- **Rodar em desenvolvimento:**
	- No diretório `frontend`, execute:
		`pnpm dev`
	- O frontend padrão estará em `http://localhost:3000`.

**Fluxo típico (desenvolvimento)**
- 1) Configure `backend/.env` e rode o backend com Uvicorn.
- 2) Configure `frontend/.env` apontando `API_URL` para o backend e rode `pnpm dev`.
- 3) Abra `http://localhost:3000` para usar a interface.

**Notas e segurança**
- Os arquivos `.env` contêm chaves sensíveis — não os comite no controle de versão. Use variáveis de ambiente seguras em produção.
- O `pyproject.toml` do backend lista as dependências; veja [backend/pyproject.toml](backend/pyproject.toml#L1-L40).

**Sobre os projetos**
- **Backend:** implementado com FastAPI, o backend expõe endpoints principais em `backend/src/main.py` (ex.: `/finance-ai` e `/init-db`). Responsabilidades:
	- Gerenciar o banco de dados SQLite (`backend/src/db`)
	- Popular dados iniciais (`seed_init.py`)
	- Gerar e atualizar o vector store usado pelo RAG (`backend/src/rag`)
	- Orquestrar agentes e pipelines de prompts em `backend/src/engine` (graph de execução)
- **Frontend:** aplicação Next.js em `frontend/` com interface React/TS. Responsabilidades:
	- UI e fluxos de chat em `frontend/src/components/Chat` e páginas em `frontend/src/app/chat`
	- Chamadas ao backend via `API_URL` em `frontend/.env`
	- Ações e contexto em `frontend/src/actions` e `frontend/src/contexts`

**Recomendações rápidas**
- Para desenvolvimento local, rode o backend em `:8000` e o frontend em `:3000`.
- Use o mesmo `API_KEY` em `backend/.env` e `frontend/.env` durante testes locais.

