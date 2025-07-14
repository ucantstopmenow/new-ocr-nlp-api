from transformers import pipeline

print("Iniciando o download dos modelos de LLM (versão online)...")

try:
    # --- NOVOS MODELOS ---
    qa_model_name = "distilbert-base-cased-distilled-squad"
    summarizer_model_name = "sshleifer/distilbart-cnn-12-6"

    # Modelo de Question-Answering
    print(f"Baixando o modelo de Q&A: {qa_model_name}")
    pipeline("question-answering", model=qa_model_name)
    print("Modelo de Q&A baixado com sucesso.")

    # Modelo de Sumarização
    print(f"Baixando o modelo de Summarization: {summarizer_model_name}")
    pipeline("summarization", model=summarizer_model_name)
    print("Modelo de Summarization baixado com sucesso.")

    print("Todos os modelos foram baixados e cacheados com sucesso!")

except Exception as e:
    print(f"Ocorreu um erro durante o download dos modelos: {e}")
    # Sai com código de erro para interromper o build do Docker se o download falhar
    exit(1)