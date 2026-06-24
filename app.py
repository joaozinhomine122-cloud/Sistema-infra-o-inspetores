import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Banco de dados local seguro
conn = sqlite3.connect('escola_aoe.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS usuarios (username TEXT PRIMARY KEY, password TEXT, nome TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS ocorrencias (id INTEGER PRIMARY KEY AUTOINCREMENT, aluno TEXT, sala TEXT, infracao TEXT, detalhes TEXT, data TEXT, registrado_por TEXT)")
conn.commit()
c.execute("INSERT OR IGNORE INTO usuarios VALUES ('admin', 'admin123', 'Administrador')")
c.execute("INSERT OR IGNORE INTO usuarios VALUES ('aoe1', 'aoe123', 'Inspetor Padrão')")
conn.commit()

st.title("🏫 Sistema de Ocorrências - AOE")

# Sistema de Login Simples na barra lateral para evitar erros de cache
st.sidebar.header("Autenticação")
usuario = st.sidebar.text_input("Usuário")
senha = st.sidebar.text_input("Senha", type="password")

if usuario == "aoe1" and senha == "aoe123":
    st.sidebar.success("Logado como: Inspetor Padrão")
    
    menu = st.sidebar.radio("Navegação", ["Painel de Alertas", "Registrar Ocorrência", "Histórico Geral"])

    if menu == "Painel de Alertas":
        st.header("🚨 Alertas Críticos (Bloqueio de Entrada)")
        df_o = pd.read_sql_query("SELECT aluno, sala FROM ocorrencias", conn)
        if not df_o.empty:
            contagem = df_o.groupby(['aluno', 'sala']).size().reset_index(name='total')
            alertas = contagem[contagem['total'] >= 2]
            if not alertas.empty:
                for idx, row in alertas.iterrows():
                    st.error(f"🛑 **{row['aluno'].upper()}** ({row['sala']}) — **{row['total']} ocorrências**. Só entra com o responsável!")
            else:
                st.success("Nenhum aluno com 2 ou mais ocorrências no momento.")
        else:
            st.info("Nenhuma ocorrência registrada ainda.")

    elif menu == "Registrar Ocorrência":
        st.header("📝 Novo Registro no Pátio")
        with st.form(key='oc_form', clear_on_submit=True):
            aluno = st.text_input("Nome do Aluno").strip()
            sala = st.selectbox("Sala", ["1º Ano", "2º Ano", "3º Ano"])
            infracao = st.selectbox("Infração", ["Desobediência direta", "Fora da sala/Quadra", "Desrespeito/Ofensa"])
            detalhes = st.text_area("Detalhes do Ocorrido")
            if st.form_submit_button("Gravar Ocorrência"):
                if aluno and detalhes:
                    dt = datetime.now().strftime("%d/%m/%Y %H:%M")
                    c.execute("INSERT INTO ocorrencias (aluno, sala, infracao, detalhes, data, registrado_por) VALUES (?,?,?,?,?,?)",
                              (aluno, sala, infracao, detalhes, dt, "Inspetor Padrão"))
                    conn.commit()
                    st.success(f"Registrado com sucesso para {aluno}!")
                else:
                    st.error("Por favor, preencha todos os campos.")

    elif menu == "Histórico Geral":
        st.header("🔍 Histórico Geral de Registros")
        df = pd.read_sql_query("SELECT data AS 'Data', aluno AS 'Aluno', sala AS 'Sala', infracao AS 'Infração', detalhes AS 'Detalhes' FROM ocorrencias ORDER BY id DESC", conn)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhum registro encontrado.")
else:
    st.warning("Por favor, digite o usuário e senha corretos na barra lateral para acessar o sistema.")
    st.info("💡 Dica de teste -> Usuário: aoe1 | Senha: aoe123")
