import sqlite3
from datetime import datetime

DATABASE_NAME = "ocorrencias.db" # Nome do novo arquivo de banco de dados

# 1. Função de Conexão e Criação de Tabela
def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # Tabela 'ocorrencias' para armazenar os dados do formulário
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ocorrencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT NOT NULL,
            data TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# 2. Função de Inserção (CREATE)
def insert_ocorrencia(titulo, descricao, status, data):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ocorrencias (titulo, descricao, status, data) 
        VALUES (?, ?, ?, ?)
    """, (titulo, descricao, status, data))
    conn.commit()
    conn.close()

def update_ocorrencia(id, titulo, descricao, status, data):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE ocorrencias 
        SET titulo = ?, descricao = ?, status = ?, data = ?
        WHERE id = ?
    """, (titulo, descricao, status, data, id))
    conn.commit()
    conn.close()

# 5. Função de Exclusão (DELETE)
def delete_ocorrencia(id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ocorrencias WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# 6. Função para obter uma única ocorrência por ID (necessário para a edição)
def get_ocorrencia_by_id(id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, descricao, status, data FROM ocorrencias WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "titulo": row[1], "descricao": row[2], "status": row[3], "data": row[4]}
    return None


# 3. Função de Leitura (READ - todas as ocorrências)
def get_all_ocorrencias():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, descricao, status, data FROM ocorrencias ORDER BY id DESC")
    # Converte os resultados em uma lista de dicionários para fácil uso
    ocorrencias_list = [
        {"id": row[0], "titulo": row[1], "descricao": row[2], "status": row[3], "data": row[4]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return ocorrencias_list

# A partir daqui, você pode adicionar funções para UPDATE e DELETE conforme o projeto avança.