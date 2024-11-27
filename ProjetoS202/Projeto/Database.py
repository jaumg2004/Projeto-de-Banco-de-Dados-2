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
            "CREATE (u:Usuario {login: $login, senha: $senha, nota_social: 0}) "
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
            "MATCH (a:Usuario {nome: $avaliador}), (b:Usuario {nome: $avaliado}) "
            "CREATE (a)-[r:AVALIA {nota: $nota, contexto: $contexto}]->(b) "
            "SET b.nota_social = (b.nota_social * (b.avaliacoes + 1) + $nota) / (b.avaliacoes + 1), "
            "b.avaliacoes = b.avaliacoes + 1 "
            "RETURN b"
        )
        tx.run(query, avaliador=avaliador, avaliado=avaliado, nota=nota, contexto=contexto)
