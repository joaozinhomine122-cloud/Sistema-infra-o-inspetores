import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Conexão com o banco de dados interno
conn = sqlite3.connect('escola_aoe.db', check_same_thread=False)
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        username TEXT PRIMARY KEY, password TEXT, nome TEXT
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS ocorrencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno TEXT, sala TEXT, infracao TEXT, detalhes TEXT, data TEXT, registrado_por TEXT
    )
''')
conn.commit()

# Criando usuários padrão se não existirem
c.execute("INSERT OR IGNORE INTO usuarios VALUES ('admin', 'admin123', 'Administrador')")
c.execute("INSERT OR IGNORE INTO usuarios VALUES ('aoe1', 'aoe123', 'Inspetor Padrão')")
conn.commit()

st.set_page_config(page_title="Sistema AOE", page_icon="🏫", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state
