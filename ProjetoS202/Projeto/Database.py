from neo4j import GraphDatabase

class SocialScoreDatabase:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def criar_usuario(self, login, senha):
        with self.driver.session() as session:
            session.write_transaction(self._criar_usuario, login, senha)

    @staticmethod
    def _criar_usuario(tx, login, senha):
        query = (
            "CREATE (u:Usuario {login: $login, senha: $senha, nota_social: 0, avaliacoes: 0}) "
            "RETURN u"
        )
        result = tx.run(query, login=login, senha=senha)
        return result.single()

    def avaliar_usuario(self, avaliador, avaliado, nota, contexto):
        with self.driver.session() as session:
            session.write_transaction(self._avaliar_usuario, avaliador, avaliado, nota, contexto)

    @staticmethod
    def _avaliar_usuario(tx, avaliador, avaliado, nota, contexto):
        query = (
            "MATCH (a:Usuario {login: $avaliador}), (b:Usuario {login: $avaliado}) "
            "CREATE (a)-[r:AVALIA {nota: $nota, contexto: $contexto}]->(b) "
            "SET b.nota_social = (b.nota_social * b.avaliacoes + $nota) / (b.avaliacoes + 1), "
            "b.avaliacoes = b.avaliacoes + 1 "
            "RETURN b"
        )
        result = tx.run(query, avaliador=avaliador, avaliado=avaliado, nota=nota, contexto=contexto)
        return result.single()

    def usuario_existe(self, login):
        with self.driver.session() as session:
            return session.read_transaction(self._usuario_existe, login)

    @staticmethod
    def _usuario_existe(tx, login):
        query = "MATCH (u:Usuario {login: $login}) RETURN COUNT(u) > 0 AS exists"
        result = tx.run(query, login=login)
        return result.single()["exists"]