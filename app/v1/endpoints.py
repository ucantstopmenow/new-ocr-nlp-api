from fastapi import APIRouter, UploadFile, File, Form, status
from fastapi.responses import JSONResponse
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone

from app.services.ocr import process_documents
from app.services.llm import get_summary, get_answer_from_docs
from app.services.database import save_log

router = APIRouter()

@router.post("/process", summary="Processa currículos com OCR e IA")
async def process_files(
    files: List[UploadFile] = File(..., description="Lista de arquivos (PDF, JPG, PNG) a serem processados."),
    request_id: Optional[UUID] = Form(default_factory=uuid4, description="ID único para rastrear a requisição."),
    user_id: str = Form(..., description="Identificador do usuário que está fazendo a requisição."),
    query: Optional[str] = Form(None, description="Pergunta específica sobre os currículos. Se omitido, será gerado um resumo de cada um.")
):
    """
    Este endpoint realiza o seguinte fluxo:
    1. Recebe um ou mais arquivos (PDF/imagem) e metadados.
    2. Extrai o texto de cada arquivo usando OCR.
    3. Se uma query for fornecida: Usa um modelo de LLM para responder à pergunta.
    4. Se a query for omitida: Usa um modelo de LLM para gerar um resumo de cada currículo.
    5. Registra um log da operação em um banco de dados não relacional para auditoria.
    """
    start_time = datetime.now(timezone.utc)

    ocr_results = await process_documents(files)

    final_results = []
    if query:
        final_results = get_answer_from_docs(query, ocr_results)
    else:
        for doc in ocr_results:
            if doc.get("text") and not doc.get("error"):
                summary = get_summary(doc["text"])
                final_results.append({
                    "filename": doc["filename"],
                    "summary": summary
                })
            else:
                 final_results.append({
                    "filename": doc["filename"],
                    "summary": None,
                    "error": doc.get("error", "Erro desconhecido durante o OCR.")
                })

    log_entry = {
        "request_id": str(request_id),
        "user_id": user_id,
        "timestamp": start_time,
        "query": query,
        "result": final_results,
        "files_processed": [f.filename for f in files]
    }
    save_log(log_entry)

    response_data = {
        "request_id": str(request_id),
        "user_id": user_id,
        "query": query,
        "results": final_results
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_data)