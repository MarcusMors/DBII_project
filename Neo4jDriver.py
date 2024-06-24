import os

from neo4j import GraphDatabase


# Clase de utilidad para manejar la sesión de Neo4j
class Neo4jDriver:
    uri = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")
    driver = 0
    def __init__(self):
        self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
        print(self.uri)
        print(self.username)
        print(self.password)

    def close(self):
        self.driver.close()

    def run_query(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            return [record for record in result]
        
    def query(self, cypher, parameters=None):
        with self.driver.session() as session:
            result = session.run(cypher, parameters)
            return [record for record in result]
    
    @staticmethod
    def get_nodes(self, limit=5):
        cypher = "MATCH (n) RETURN n LIMIT $limit"
        return self.query(cypher, {"limit": limit})
