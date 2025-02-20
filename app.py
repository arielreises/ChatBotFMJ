import streamlit as st
import sqlite3
from datetime import datetime, timedelta
from backend import salvar_paciente, obter_pacientes, obter_pacientes_para_notificacao, enviar_mensagem_whatsapp

# Configuração da Página
st.title("Cadastro para Exame de Colonoscopia")

# Formulário de Cadastro
with st.form(key="cadastro"):
    nome = st.text_input("Nome Completo")
    idade = st.number_input("Idade", min_value=18, max_value=120, step=1)
    telefone = st.text_input("Telefone (com DDD)")
    data_exame = st.date_input("Data do Exame", min_value=datetime.today())

    submit = st.form_submit_button("Cadastrar")

    if submit:
        salvar_paciente(nome, idade, telefone, data_exame)
        st.success("Paciente cadastrado com sucesso!")

# Exibir Agenda
st.subheader("Pacientes Agendados")
pacientes = obter_pacientes()

if pacientes:
    for paciente in pacientes:
        st.write(f"📅 {paciente[1]} - {paciente[2]} anos - 📞 {paciente[3]} - 🏥 Exame em {paciente[4]}")
else:
    st.write("Nenhum paciente agendado.")

# Botão para Disparar Mensagens
if st.button("Disparar Mensagens Agendadas"):
    pacientes_para_notificar = obter_pacientes_para_notificacao()
    for paciente in pacientes_para_notificar:
        enviar_mensagem_whatsapp(paciente[3], paciente[1], paciente[4])
    st.success("Mensagens enviadas para os pacientes agendados.")
