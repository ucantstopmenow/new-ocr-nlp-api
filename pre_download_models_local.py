from transformers import pipeline
import os

# --- NOVOS MODELOS, MAIS POPULARES E EM INGLÊS ---
qa_model_name = "distilbert-base-cased-distilled-squad"
summarizer_model_name = "sshleifer/distilbart-cnn-12-6"

# Diretórios de destino
qa_model_path = "./models/question-answering"
summarizer_model_path = "./models/summarization"

print("Iniciando o download dos modelos para o diretório local...")
print(f"-> Q&A Model: {qa_model_name}")
print(f"-> Summarization Model: {summarizer_model_name}")


try:
    os.makedirs(qa_model_path, exist_ok=True)
    os.makedirs(summarizer_model_path, exist_ok=True)
    
    print(f"\nBaixando modelo de Q&A...")
    qa_pipeline = pipeline("question-answering", model=qa_model_name)
    qa_pipeline.save_pretrained(qa_model_path)
    print(f"Modelo de Q&A salvo em: {qa_model_path}")

    print(f"\nBaixando modelo de Sumarização...")
    summarizer_pipeline = pipeline("summarization", model=summarizer_model_name)
    summarizer_pipeline.save_pretrained(summarizer_model_path)
    print(f"Modelo de Sumarização salvo em: {summarizer_model_path}")

    print("\n✅ Download e salvamento de todos os modelos concluídos com sucesso!")

except Exception as e:
    print(f"\n❌ Ocorreu um erro durante o download: {e}")
    print("\n[INVESTIGAÇÃO] O problema parece ser de rede. Veja as dicas abaixo.")