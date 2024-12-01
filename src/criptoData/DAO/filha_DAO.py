import sqlite3
from datetime import datetime
from criptoData.dados.filha import Filha

class FilhaDAO:
    def __init__(self, db_name="database.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS filha (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idMae INTEGER NOT NULL,
            dataInclusao DATETIME NOT NULL,
            dataExclusao DATETIME,
            FOREIGN KEY (idMae) REFERENCES mae(id)
        )
        """
        self.conn.execute(query)

    def inserir(self, filha):
        query = "INSERT INTO filha (nome, idMae, dataInclusao) VALUES (?, ?, ?)"
        now = datetime.now()
        self.conn.execute(query, (filha.nome, filha.idMae, now))
        self.conn.commit()

    def alterar(self, id, novo_nome):
        now = datetime.now()
        self.conn.execute("UPDATE filha SET dataExclusao = ? WHERE id = ?", (now, id))
        filha_antiga = self.conn.execute("SELECT idMae FROM filha WHERE id = ?", (id,)).fetchone()
        if filha_antiga:
            idMae = filha_antiga[0]
            self.inserir(Filha(nome=novo_nome, idMae=idMae))

    def excluir(self, id):
        now = datetime.now()
        self.conn.execute("UPDATE filha SET dataExclusao = ? WHERE id = ?", (now, id))
        self.conn.commit()

    def consultar(self):
        query = "SELECT id, nome, idMae, dataInclusao, dataExclusao FROM filha WHERE dataExclusao IS NULL"
        cursor = self.conn.execute(query)
        return [Filha(*row) for row in cursor]
