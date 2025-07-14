from typing import List, Dict

_YOUTUBE_PIPELINE = None
_SUMMARIZER_PIPELINE = None

def _init_pipelines():
    global _YOUTUBE_PIPELINE, _SUMMARIZER_PIPELINE
    if _YOUTUBE_PIPELINE is None or _SUMMARIZER_PIPELINE is None:
        try:
            from transformers import pipeline

            # --- Usa os nomes dos novos modelos para carregar em memória ---
            _YOUTUBE_PIPELINE = pipeline(
                "question-answering",
                model="distilbert-base-cased-distilled-squad" 
            )
            _SUMMARIZER_PIPELINE = pipeline(
                "summarization",
                model="sshleifer/distilbart-cnn-12-6"
            )
            print("Pipelines de LLM carregadas com sucesso a partir do cache.")
        except Exception as e:
            print(f"Erro ao inicializar pipelines de LLM: {e}")
            _YOUTUBE_PIPELINE = _SUMMARIZER_PIPELINE = None

# O resto do arquivo (get_summary, get_answer_from_docs) permanece o mesmo que o original
def get_summary(text: str) -> str:
    _init_pipelines()
    if not _SUMMARIZER_PIPELINE:
        return "Serviço de resumo indisponível."
    if not text or len(text.strip()) < 100:
        return text.strip()

    max_chunk_size = 1024
    chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]

    summary_parts = []
    for chunk in chunks:
        try:
            summary = _SUMMARIZER_PIPELINE(
                chunk,
                max_length=150,
                min_length=40,
                do_sample=False,
            )
            summary_parts.append(summary[0]["summary_text"])
        except Exception:
            continue

    return " ".join(summary_parts)


def get_answer_from_docs(query: str, documents: List[Dict]) -> List[Dict]:
    _init_pipelines()
    responses: List[Dict] = []

    for doc in documents:
        if doc.get("text") and not doc.get("error"):
            if not _YOUTUBE_PIPELINE:
                responses.append({
                    "filename": doc["filename"],
                    "answer": "Serviço de Q&A indisponível.",
                    "score": 0,
                    "justification": "O modelo de linguagem não pôde ser carregado.",
                })
            else:
                try:
                    result = _YOUTUBE_PIPELINE(question=query, context=doc["text"])
                    responses.append({
                        "filename": doc["filename"],
                        "answer": result.get("answer", ""),
                        "score": result.get("score", 0),
                        "justification": f"Encontrado com confiança de {result.get('score', 0):.2%}.",
                    })
                except Exception as e:
                    responses.append({
                        "filename": doc["filename"],
                        "answer": "Erro durante Q&A.",
                        "score": 0,
                        "justification": str(e),
                    })
        else:
            responses.append({
                "filename": doc.get("filename", ""),
                "answer": "Não foi possível analisar este documento.",
                "score": 0,
                "justification": doc.get("error", "Texto não extraído."),
            })

    return sorted(responses, key=lambda x: x.get("score", 0), reverse=True)