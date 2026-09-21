from fastapi import FastAPI, HTTPException
from models import PessoaCreate, PhaseUpdate
import pipefy_client

app = FastAPI(title="Profectum API Integração Pipefy")

@app.post("/pessoas", status_code=201)
async def criar_pessoa(pessoa: PessoaCreate):
    response = await pipefy_client.create_card(pessoa.dict())
    if "errors" in response:
        raise HTTPException(status_code=400, detail=response["errors"])
    return response["data"]["createCard"]["card"]

@app.delete("/pessoas/{card_id}")
async def deletar_pessoa(card_id: str):
    response = await pipefy_client.delete_card(card_id)
    if "errors" in response:
        raise HTTPException(status_code=400, detail=response["errors"])
    return {"message": "Card deletado com sucesso", "success": response["data"]["deleteCard"]["success"]}

@app.put("/pessoas/{card_id}/fase")
async def alterar_fase_pessoa(card_id: str, phase: PhaseUpdate):
    response = await pipefy_client.move_card_to_phase(card_id, phase.phase_id)
    if "errors" in response:
        raise HTTPException(status_code=400, detail=response["errors"])
    
    card_info = response["data"]["moveCardToPhase"]["card"]
    current_phase = card_info["current_phase"]
    
    result = {
        "message": f"Card movido para a fase {current_phase['name']}",
        "card": card_info
    }
    
    if current_phase.get("done") is True or str(current_phase.get("id")) == "323403004":
        result["info_adicional"] = "O processo desta pessoa foi finalizado e o card chegou na fase fim."
        
    return result
