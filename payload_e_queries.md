# Payload e Consultas de Engenharia Reversa

Este documento guarda os utilitários usados durante a construção e teste da API de integração com o Pipefy.

## 📦 Payload Pré-Pronto para Teste

Este é um payload em formato JSON com dados fictícios, mas 100% formatados nas regras de negócio exigidas pelo formulário do Pipefy.
Você pode usá-lo diretamente na rota `POST /pessoas` do Swagger (`http://127.0.0.1:8000/docs`).

```json
{
  "nome": "Candidato Profectum Teste",
  "data_de_nascimento": "1995-05-15",
  "cpf": "551.780.658-91",
  "telefone": "(11) 98765-4321",
  "data": "2026-09-21T10:00:00-03:00",
  "sexo": "Masculino",
  "hobbies": [
    "Esportes",
    "Leitura"
  ],
  "cidade": [
    "850256930"
  ]
}
```
*Nota: O CPF incluído foi gerado aleatoriamente mas com dígito verificador matemático real para passar pela validação do Pipefy. O ID da cidade (850256930) refere-se à cidade de "Fortaleza" e os hobbies listados fazem parte da predefinição do formulário.*

---

## 🔍 Consultas GraphQL (Engenharia Reversa)

Como o case forneceu as credenciais (Token e Pipe ID) mas as informações deveriam ser descobertas, disparamos consultas cruas via GraphQL para a API do Pipefy ( `https://api.pipefy.com/graphql` ) para mapear os dados necessários antes de codificarmos a API em Python.

### 1. Mapeamento de Campos e Fases
Essa query foi utilizada para listar todos os identificadores (IDs) internos exigidos pelo cadastro de Pessoa, os tipos de dados aceitos (ex: `date`, `cpf`, `connector`) e descobrir o ID de cada etapa do processo (incluindo a "Fase Fim").

```graphql
query {
  pipe(id: 303843596) {
    name
    start_form_fields {
      id
      label
      type
    }
    phases {
      id
      name
      done
    }
  }
}
```

### 2. Mapeamento dos IDs de Conectores (Cidades)
O campo cidade era um conector, exigindo o ID de um card do banco de dados atrelado (e não uma string de texto simples). Para não precisarmos acessar a plataforma visual e copiarmos o link na interface, disparamos uma query para analisar os últimos candidatos cadastrados e farejar quais os valores em array (`array_value`) foram utilizados pelos outros usuários:

```graphql
query {
  allCards(pipeId: 303843596, first: 20) {
    edges {
      node {
        id
        title
        fields {
          name
          value
          array_value
        }
      }
    }
  }
}
```
*Resultado obtido:* O `array_value` de campos como `Cidade` nesses relatórios antigos retornou as conexões reais, de onde extraímos códigos seguros como `850256930` (Fortaleza).*
