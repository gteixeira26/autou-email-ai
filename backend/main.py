from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from textblob import TextBlob
import fitz
import chardet
import re
import unicodedata

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

def normalize_text(text):
    text = text.lower()
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text.strip()

def strip_salutation(text):
    return re.sub(r"^(ola|oi|bom dia|boa tarde|boa noite|tudo bem)\b[\s,]*", "", text)

def contains_keyword(text, keywords):
    for kw in keywords:
        if re.search(rf'\b{re.escape(kw)}\b', text):
            return True
    return False

@app.post("/analyze/")
async def analyze_email(file: UploadFile = File(None), text: str = Form(None)):
    if file:
        if file.filename.lower().endswith(".pdf"):
            email_text = extract_text_from_pdf(file)
        elif file.filename.lower().endswith(".txt"):
            email_text = extract_text_from_txt(file)
        else:
            return {"error": "Formato de arquivo não suportado."}
    elif text:
        email_text = text
    else:
        return {"error": "Nenhum conteúdo fornecido."}

    email_lower = normalize_text(email_text)
    email_core = strip_salutation(email_lower)

    if contains_keyword(email_lower, ["feliz natal", "boas festas", "parabens", "feriado"]):
        return {"category": "Improdutivo", "response": "Agradecemos pelos votos! Desejamos um excelente dia também. 🎉"}

    if contains_keyword(email_lower, ["obrigado", "agradecido", "valeu", "elogio", "agradecer"]):
        return {"category": "Improdutivo", "response": "Agradecemos seu retorno! Ficamos felizes em ajudar. 😊"}

    if contains_keyword(email_core, ["fatura", "pagamento", "boleto", "cobranca", "credito", "debito", "extrato"]):
        return {"category": "Produtivo", "response": "Entendemos sua solicitação financeira. Em breve retornaremos com mais detalhes."}

    if contains_keyword(email_core, [
        "suporte", "erro", "problema", "falha", "acesso", "ajuda",
        "preciso de ajuda", "apoio", "assistencia", "gostaria de ajuda",
        "gostaria de um suporte", "preciso de suporte", "solicito suporte",
        "necessito de ajuda"
    ]):
        return {"category": "Produtivo", "response": "Olá! Seu pedido de suporte foi registrado. Um de nossos especialistas irá ajudá-lo em breve."}

    if contains_keyword(email_core, ["task", "demanda", "caso", "protocolo", "ticket", "status"]):
        return {"category": "Produtivo", "response": "Recebemos sua solicitação e vamos verificar o status para você."}

    if contains_keyword(email_core, ["duvida", "pergunta"]):
        return {"category": "Produtivo", "response": "Recebemos sua dúvida! Em breve entraremos em contato com a resposta. 🤝"}

    sentiment = TextBlob(email_text).sentiment.polarity
    if sentiment < -0.1:
        return {"category": "Produtivo", "response": "Olá! Recebemos sua mensagem e estamos analisando. Em breve entraremos em contato."}

    return {"category": "Improdutivo", "response": "Obrigado pelo contato! Conte conosco sempre que precisar. 😄"}
