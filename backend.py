import sqlite3
from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

# Criar banco de dados
def criar_bd():
    conn = sqlite3.connect("pacientes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            idade INTEGER,
            telefone TEXT,
            data_exame DATE
        )
    """)
    conn.commit()
    conn.close()

# Salvar paciente no banco
def salvar_paciente(nome, idade, telefone, data_exame):
    conn = sqlite3.connect("pacientes.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pacientes (nome, idade, telefone, data_exame) VALUES (?, ?, ?, ?)", 
                   (nome, idade, telefone, data_exame))
    conn.commit()
    conn.close()

# Obter todos os pacientes
def obter_pacientes():
    conn = sqlite3.connect("pacientes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pacientes ORDER BY data_exame")
    pacientes = cursor.fetchall()
    conn.close()
    return pacientes

# Obter pacientes com exames em 7, 2 ou 1 dia
def obter_pacientes_para_notificacao():
    hoje = datetime.today().date()
    dias_notificar = [7, 2, 1]
    
    conn = sqlite3.connect("pacientes.db")
    cursor = conn.cursor()
    consulta = f"""
        SELECT * FROM pacientes WHERE 
        julianday(data_exame) - julianday('{hoje}') IN ({','.join(map(str, dias_notificar))})
    """
    cursor.execute(consulta)
    pacientes = cursor.fetchall()
    conn.close()
    
    return pacientes

# Enviar mensagem pelo WhatsApp API
def enviar_mensagem_whatsapp(telefone, nome, data_exame):
    url = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    mensagem = f"Olá {nome}, lembramos que seu exame de colonoscopia está agendado para {data_exame}. Caso precise remarcar, entre em contato."
    
    data = {
        "messaging_product": "whatsapp",
        "to": telefone,
        "type": "text",
        "text": {"body": mensagem}
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Criar banco ao iniciar
criar_bd()
