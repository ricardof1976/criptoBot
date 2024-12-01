import sqlite3
from datetime import datetime
from criptoData.dados.mae import Mae

class MaeDAO:
    def __init__(self, db_name="database.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS mae (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            dataInclusao DATETIME NOT NULL,
            dataExclusao DATETIME
        )
        """
        self.conn.execute(query)

    def inserir(self, mae):
        query = "INSERT INTO mae (nome, dataInclusao) VALUES (?, ?)"
        now = datetime.now()
        self.conn.execute(query, (mae.nome, now))
        self.conn.commit()

    def alterar(self, id, novo_nome):
        now = datetime.now()
        self.conn.execute("UPDATE mae SET dataExclusao = ? WHERE id = ?", (now, id))
        self.inserir(Mae(nome=novo_nome))

    def excluir(self, id):
        now = datetime.now()
        self.conn.execute("UPDATE mae SET dataExclusao = ? WHERE id = ?", (now, id))
        self.conn.commit()

    def consultar(self):
        query = "SELECT id, nome, dataInclusao, dataExclusao FROM mae WHERE dataExclusao IS NULL"
        cursor = self.conn.execute(query)
        return [Mae(*row) for row in cursor]
