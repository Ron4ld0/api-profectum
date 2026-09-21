# 🚀 API de Integração com Pipefy - Case Profectum

Este repositório contém a resolução do Case Técnico da Profectum para a construção de uma API em Python integrada à plataforma Pipefy. A API é responsável por orquestrar o gerenciamento (Criação, Movimentação de Fases e Exclusão) da entidade **"Pessoa"** utilizando chamadas assíncronas ao GraphQL do Pipefy.

---

## 🛠️ Tecnologias Utilizadas

Para garantir alta performance, validação robusta e um fluxo assíncrono nativo, o projeto foi construído com as seguintes tecnologias:

- **[FastAPI](https://fastapi.tiangolo.com/):** Framework web ultra-rápido para construção da API.
- **[Uv](https://github.com/astral-sh/uv):** Gerenciador de dependências e ambiente virtual ultra-rápido em Rust, substituindo o pip/venv tradicional.
- **[Httpx](https://www.python-httpx.org/):** Cliente HTTP assíncrono para consumo das Queries e Mutations do GraphQL do Pipefy.
- **[Pydantic](https://docs.pydantic.dev/):** Tipagem de dados e validações estritas do payload recebido nos endpoints.

---

## ⚙️ Como Instalar e Rodar Localmente

### 1. Pré-requisitos
- Ter o instalador **uv** configurado na sua máquina (caso não tenha, pode instalar facilmente pela documentação oficial da Astral).
- Obter o **Token de Autenticação** da sua conta do Pipefy.

### 2. Configurando o Ambiente
Clone este repositório e crie um arquivo `.env` na raiz do projeto com as suas credenciais:

```env
PIPEFY_TOKEN=seu_token_aqui_gerado_no_pipefy
PIPE_ID=303843596
```

### 3. Rodando a Aplicação
Graças ao `uv`, não é necessário rodar comandos morosos de criação de virtual envs. Basta rodar o comando abaixo para que o uv instale tudo e suba o servidor de desenvolvimento instantaneamente:

```bash
uv run uvicorn main:app --reload
```

Acesse **[http://localhost:8000/docs](http://localhost:8000/docs)** para abrir o painel interativo do Swagger e testar a API!

---

## 📡 Endpoints Desenvolvidos

Abaixo estão os 3 endpoints solicitados no desafio:

### 🟢 `POST /pessoas` - Criar Candidato
Aciona a mutation `createCard` para alocar o candidato diretamente na fase "Caixa de Entrada".
* **Atenção aos tipos estritos do Pipefy:**
  * O `CPF` passa por cálculo validador do Pipefy. Use um CPF válido.
  * O campo `cidade` é um **conector**, ou seja, exige que o ID passado na lista seja um ID real de uma cidade cadastrada no banco de dados do Pipefy.
  * Os `hobbies` devem corresponder a lista de opções exatas do seu checklist lá no painel.

### 🔵 `PUT /pessoas/{card_id}/fase` - Alterar Fase
Mapeado para mover o card para uma fase destino (`moveCardToPhase`).
* **Interceptador Inteligente:** Caso a fase destino informada seja exatamente a fase fim do processo (Concluído), a nossa API devolve junto ao payload do card uma mensagem bônus: `"O processo desta pessoa foi finalizado e o card chegou na fase fim."`.

### 🔴 `DELETE /pessoas/{card_id}` - Excluir Card
Envia o comando `deleteCard` para o sistema e confirma a limpeza do registro do Pipefy.

---

> Desenvolvido com ☕ e Python durante processo de case técnico!
