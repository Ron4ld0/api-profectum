# 🚀 Apresentação: Integração com Pipefy - Case Técnico Profectum

Este documento detalha o processo de desenvolvimento, as decisões técnicas e as funcionalidades implementadas para atender integralmente aos requisitos propostos no Case Técnico de Integração com o Pipefy.

---

## 🎯 1. Entendimento do Desafio

O objetivo principal do case era construir uma API em Python capaz de gerenciar a entidade "Pessoa" dentro do Pipefy, fornecendo um fluxo contínuo de:
- **Criação de Cards** com dados específicos.
- **Movimentação de Fases**, identificando quando o processo chegava ao fim.
- **Exclusão de Cards** a partir de um ID.

Como diferencial metodológico, o case exigia não apenas codificar, mas realizar a **descoberta dos campos** no GraphQL do Pipefy, exigindo a compreensão ativa da sua estrutura de dados.

---

## 🛠️ 2. Escolhas Tecnológicas e Arquitetura

Para garantir uma API robusta, rápida e em conformidade com as melhores práticas de mercado atual, optei pelo seguinte stack:

- **FastAPI**: Framework escolhido por sua altíssima performance, documentação interativa automática (Swagger) e validações nativas robustas com tipagem em Python.
- **Uv**: Gerenciador de dependências e ambiente ultra-rápido, assegurando uma instalação limpa, livre de conflitos e isolada em uma pasta `.venv`.
- **Httpx**: Biblioteca para requisições HTTP assíncronas. Como o FastAPI brilha no processamento assíncrono, optamos por `httpx` ao invés de `requests` padrão, evitando bloquear o *Event Loop* durante a comunicação com a API do Pipefy.
- **Pydantic**: Responsável por validar e tipar rigidamente os dados de entrada (payloads) fornecidos pelos usuários da API antes de enviá-los ao Pipefy.

**Arquitetura do Projeto:**
O código foi modularizado para facilitar a manutenção e escalabilidade:
1. `models.py`: Entidades Pydantic isoladas.
2. `pipefy_client.py`: Camada de serviço, 100% isolada e dedicada à formatação e execução das Queries/Mutations do GraphQL.
3. `main.py`: Camada de controladores (Endpoints FastAPI), responsável por receber as requisições e devolver o output formatado.
4. `.env`: Variáveis de ambiente garantindo a segurança dos Tokens e IDs.

---

## 🔎 3. Estudo e Descoberta (Engenharia Reversa da API)

Antes de programar os endpoints, realizamos uma requisição GraphQL investigativa apontada para o Pipe disponibilizado (`ID: 303843596`).
A query de exploração nos retornou exatamente o mapeamento estrutural exigido para o cadastro de "Pessoa":

**Campos Mapeados (`start_form_fields`):**
- `nome` (short_text)
- `data_de_nascimento` (date)
- `cpf` (cpf)
- `telefone` (phone)
- `data` (datetime)
- `sexo` (radio_vertical)
- `hobbies` (checklist_vertical) - *Exige array com opções predefinidas.*
- `cidade` (connector) - *Exige o ID do card num banco de dados relacional.*

**Fases Mapeadas:**
- `323403002`: Caixa de entrada
- `323403003`: Fazendo
- `323403004`: Concluído (**Fase Fim / done: true**)

---

## ⚙️ 4. Desenvolvimento dos Requisitos (Endpoints)

Com base no mapeamento, construímos a solução de forma 100% alinhada aos requisitos.

### 🟢 A. Endpoint de Criação (`POST /pessoas`)
- **Como funciona:** Recebe um JSON do usuário através do modelo Pydantic `PessoaCreate`.
- **Validação:** Todos os campos foram tipados.
- **Integração:** Transforma os dados numa lista de `fields_attributes` e dispara a mutation `createCard` do GraphQL para alocar o cadastro diretamente na fase inicial ("Caixa de entrada").

### 🟡 B. Endpoint de Exclusão (`DELETE /pessoas/{card_id}`)
- **Como funciona:** Recebe o identificador numérico único do card pela rota.
- **Integração:** Aciona a mutation `deleteCard` passando o ID do candidato, garantindo o sumiço do registro em definitivo.

### 🔵 C. Endpoint de Avanço e Fase Fim (`PUT /pessoas/{card_id}/fase`)
- **Como funciona:** Recebe o novo ID da fase destino pelo Body da requisição e o ID do card pela Rota. Aciona a mutation `moveCardToPhase`.
- **A Cereja do Bolo (Requisito Fim):** Ao obter a resposta de sucesso da Pipefy, a API inspeciona o objeto `current_phase` recebido.
- **Lógica Inteligente:** Verificamos se o nó devolveu `done: true` ou se o ID era especificamente o de "Concluído" (`323403004`). Se positivo, a API enriquece o JSON de retorno incluindo a propriedade:
  > `"info_adicional": "O processo desta pessoa foi finalizado e o card chegou na fase fim."`

---

## 🧪 5. Validações e Testes Finais

Como prova de funcionamento:
1. O payload gerado pelo backend é serializado perfeitamente para as regras de GraphQL do Pipefy.
2. A API lida e repassa erros de regras de negócio estritas do Pipefy. Por exemplo, se fornecermos um CPF de testes em formato inválido ou uma cidade inexistente no conector, nossa API repassa com clareza o erro formatado sem causar quebra do sistema (Erro `400 Bad Request`).
3. O projeto tem a execução documentada por completo via interface interativa Swagger no `/docs`.

**A solução se mostra modular, assíncrona, focada em regras de negócio e preparada para fácil escalabilidade!**
