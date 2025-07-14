from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.v1.endpoints import router as v1_router

app = FastAPI(
    title="Currículo AI",
    description="OCR e LLM para currículos",
    version="1.0.0",
    debug=True
)

# Adicionado para corrigir o erro "Failed to fetch" (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restrinja para origens conhecidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raiz para verificar se a API está no ar."""
    return {"status": "API Currículo AI está funcionando!"}