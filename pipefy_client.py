import os
import httpx
from dotenv import load_dotenv

load_dotenv()

PIPEFY_TOKEN = os.getenv("PIPEFY_TOKEN")
PIPE_ID = os.getenv("PIPE_ID")
API_URL = "https://api.pipefy.com/graphql"

headers = {
    "Authorization": f"Bearer {PIPEFY_TOKEN}",
    "Content-Type": "application/json"
}

async def create_card(data: dict):
    fields_attributes = [
        {"field_id": "nome", "field_value": data.get("nome")},
        {"field_id": "data_de_nascimento", "field_value": data.get("data_de_nascimento")},
        {"field_id": "cpf", "field_value": data.get("cpf")},
        {"field_id": "telefone", "field_value": data.get("telefone")},
        {"field_id": "data", "field_value": data.get("data")},
        {"field_id": "sexo", "field_value": data.get("sexo")},
        {"field_id": "hobbies", "field_value": data.get("hobbies")},
        {"field_id": "cidade", "field_value": data.get("cidade")}
    ]
    
    query = """
    mutation CreateCard($pipe_id: ID!, $fields: [FieldValueInput]) {
      createCard(input: {pipe_id: $pipe_id, fields_attributes: $fields}) {
        card {
          id
          title
          current_phase {
            id
            name
          }
        }
      }
    }
    """
    
    variables = {
        "pipe_id": PIPE_ID,
        "fields": fields_attributes
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, headers=headers, json={"query": query, "variables": variables})
        return response.json()

async def delete_card(card_id: str):
    query = """
    mutation DeleteCard($card_id: ID!) {
      deleteCard(input: {id: $card_id}) {
        success
      }
    }
    """
    
    variables = {
        "card_id": card_id
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, headers=headers, json={"query": query, "variables": variables})
        return response.json()

async def move_card_to_phase(card_id: str, destination_phase_id: int):
    query = """
    mutation MoveCard($card_id: ID!, $destination_phase_id: ID!) {
      moveCardToPhase(input: {card_id: $card_id, destination_phase_id: $destination_phase_id}) {
        card {
          id
          current_phase {
            id
            name
            done
          }
        }
      }
    }
    """
    
    variables = {
        "card_id": card_id,
        "destination_phase_id": destination_phase_id
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, headers=headers, json={"query": query, "variables": variables})
        return response.json()
