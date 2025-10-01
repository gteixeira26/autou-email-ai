from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
import fitz
import chardet

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    device=-1
)

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_txt(file):
    raw_data = file.file.read()
    encoding = chardet.detect(raw_data)["encoding"]
    return raw_data.decode(encoding)

@app.post("/analyze/")
async def analyze_email(file: UploadFile = File(None), text: str = Form(None)):
    if file:
        if file.filename.endswith(".pdf"):
            email_text = extract_text_from_pdf(file)
        elif file.filename.endswith(".txt"):
            email_text = extract_text_from_txt(file)
        else:
            return {"error": "Formato de arquivo não suportado."}
    elif text:
        email_text = text
    else:
        return {"error": "Nenhum conteúdo fornecido."}

    email_lower = email_text.lower()

    if any(kw in email_lower for kw in ["feliz natal", "boas festas", "parabéns", "feriado"]):
        category = "Improdutivo"
        response = "Agradecemos pelos votos! Desejamos um excelente dia também. 🎉"
    elif any(kw in email_lower for kw in ["obrigado", "agradecido", "valeu"]):
        category = "Improdutivo"
        response = "Agradecemos seu retorno! Ficamos felizes em ajudar. 😊"
    elif any(kw in email_lower for kw in ["bom dia", "boa tarde", "boa noite", "oi", "olá", "tudo bem"]):
        category = "Improdutivo"
        response = "Agradecemos sua mensagem! Estamos à disposição caso precise de algo. 😉"
    else:
        result = classifier(email_text[:512])[0]
        label = result["label"]
        if label == "NEGATIVE":
            category = "Produtivo"
            if any(word in email_lower for word in ["suporte", "erro", "problema", "falha", "acesso"]):
                response = "Olá! Seu pedido de suporte foi registrado. Um de nossos especialistas irá ajudá-lo em breve."
            elif any(word in email_lower for word in ["task", "demanda", "caso", "protocolo", "ticket"]):
                response = "Confirmamos o recebimento da sua solicitação. Estamos acompanhando e retornaremos em breve."
            elif any(word in email_lower for word in ["dúvida", "pergunta"]):
                response = "Recebemos sua dúvida! Nossa equipe irá respondê-la o mais rápido possível. 🤝"
            else:
                response = "Olá! Recebemos sua mensagem e estamos analisando. Em breve entraremos em contato."
        else:
            category = "Improdutivo"
            response = "Obrigado pelo contato! Conte conosco sempre que precisar. 😄"

    return {
        "category": category,
        "response": response
    }
