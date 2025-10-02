📬 AutoU Email AI – Classificador Inteligente de Emails

Olá! Esse projeto foi desenvolvido para o desafio técnico da AutoU, com o objetivo de facilitar o trabalho de equipes que recebem muitos emails diariamente. Ele permite:

📎 Upload de arquivos .txt ou .pdf (ou colar o texto diretamente);

🤖 Classificação automática do email como Produtivo ou Improdutivo;

✉️ Geração de uma resposta automática baseada no conteúdo;

🌗 Interface com modo claro/escuro para uma navegação agradável.

⚙️ Como rodar localmente
Pré-requisitos

Python 3.9+

Git

1. Clone o repositório
git clone https://github.com/gteixeira26/autou-email-ai.git
cd autou-email-ai

2. Rodar o Backend (API)
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000


Isso vai rodar o servidor localmente em http://localhost:8000.

3. Abrir o Frontend
cd ../frontend


Abra o arquivo index.html no seu navegador (pode clicar duas vezes ou usar o VSCode com Live Server).

🧠 Como a IA funciona

Foi utilizada a biblioteca TextBlob para análise de sentimentos.

A classificação é baseada em palavras-chave e contexto — útil para diferenciar mensagens como:

“Preciso de ajuda com o sistema” → Produtivo

“Feliz Natal!” → Improdutivo

☁️ Deploy

A aplicação completa está hospedada em ambiente AWS (EC2 + Nginx + Certbot). Link:

👉 https://autouprojeto.xyz

📁 Estrutura
autou-email-ai/
│
├── backend/         # API FastAPI
│   ├── main.py      # Lógica de classificação e resposta
│   └── requirements.txt
│
└── frontend/        # HTML + JS + CSS
    └── index.html   # Interface Web
