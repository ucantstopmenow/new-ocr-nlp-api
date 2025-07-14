from paddleocr import PaddleOCR
from pdf2image import convert_from_bytes
from fastapi import UploadFile
from typing import List
from io import BytesIO
import filetype
from PIL import Image
import numpy as np

# Inicialize o motor OCR fora da função para maior eficiência
ocr_engine = PaddleOCR(use_angle_cls=True, lang='pt')

async def process_documents(files: List[UploadFile]):
    """
    Processa uma lista de arquivos (PDF ou Imagem) e extrai o texto usando OCR.
    """
    results = []
    for file in files:
        content = await file.read()
        kind = filetype.guess(content)
        filename = file.filename

        text = ""
        error = None

        try:
            # Processa se for PDF
            if filename.lower().endswith(".pdf"):
                images = convert_from_bytes(content)
                full_text = []
                for image in images:
                    page_text = perform_ocr_on_image(image)
                    full_text.append(page_text)
                text = "\n\n--- Próxima Página ---\n\n".join(full_text)

            # Processa se for Imagem
            elif kind and kind.mime.startswith("image/"):
                image = Image.open(BytesIO(content))
                text = perform_ocr_on_image(image)
            
            else:
                error = "Tipo de arquivo não suportado. Use PDF, JPG ou PNG."

        except Exception as e:
            error = f"Erro ao processar o arquivo: {str(e)}"

        results.append({"filename": filename, "text": text.strip(), "error": error})

    return results

def perform_ocr_on_image(image: Image.Image) -> str:
    """
    Executa OCR em um objeto de imagem PIL, com pré-processamento, sem salvar em disco.
    """
    # 1. Pré-processamento: converte para RGB (padrão esperado) e depois para array numpy
    image = image.convert("RGB")
    
    # Converte a imagem PIL para um array numpy, que é o formato que o PaddleOCR aceita
    img_np = np.array(image)

    # 2. Executa OCR diretamente no array da imagem
    result = ocr_engine.ocr(img_np)
    
    # 3. Extrai e junta o texto
    lines = []
    if result and result[0] is not None:
        for line_data in result[0]:
            # line_data é uma tupla como ([(x1, y1), ...], ('texto', 0.99))
            lines.append(line_data[1][0])
            
    return "\n".join(lines).strip()