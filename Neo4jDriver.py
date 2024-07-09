
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


def construct_raw_query(query, parameters):
    for key, value in parameters.items():
        if isinstance(value, str):
            value = f"{value}"
        query = query.replace(f"${key}", str(value))
    return query

# Clase de utilidad para manejar la sesión de Neo4j
class Neo4jDriver:
    def __init__(self):
        load_dotenv()
        self.uri = os.getenv("NEO4J_URI")
        self.username = os.getenv("NEO4J_USERNAME")
        self.password = os.getenv("NEO4J_PASSWORD")
        print("-----------------------------------------------------------------")
        print(self.uri,self.username,self.password)
        print("-----------------------------------------------------------------")
        self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
        print(self.uri)
        print(self.username)
        print(self.password)

    def close(self):
        self.driver.close()

    def query(self, cypher, parameters=None):
        print(f"{parameters = }")
        with self.driver.session() as session:
            result = session.run(cypher, parameters)
            return [record for record in result]

    @staticmethod
    def get_nodes(self, limit=5):
        cypher = "MATCH (n) RETURN n LIMIT $limit"
        return self.query(cypher, {"limit": limit})

    @staticmethod
    def get_canciones_de_genero_kpop(self, limit=5):
        cypher = (
            "MATCH (c:Cancion)-[:PERTENECE_A]->(g1:Genero {nombre: 'k-pop'})"
            "RETURN c.track_name AS names LIMIT $limit"
            )
        return self.query(cypher, {"limit": limit})

    @staticmethod
    def get_canciones_de_genero_anime(self, limit=5):
        cypher = (
            "MATCH (c:Cancion)-[:PERTENECE_A]->(g1:Genero {nombre: 'anime'}) "
            "RETURN c.track_name AS names LIMIT 5 "
            )
        # cypher = (
        #     "MATCH (c:Cancion)-[:PERTENECE_A]->(g1:Genero {nombre: 'anime'})"
        #     "RETURN c.track_name AS names LIMIT $limit"
        #     )
        return self.query(cypher, {"limit": limit})

    @staticmethod
    def search_artists(self, search_string , limit=5):
        cypher = (
        "MATCH (n:Artista)"
        "WHERE n.nombre contains $search_string"
        "RETURN n.nombre AS names LIMIT $limit"
        )
        return self.query(cypher, {"limit": limit})

    @staticmethod
    def search_songs(self, search_string , limit=5):
        # cypher = (
        # "MATCH (cancion:Cancion) "
        # "WHERE toLower(cancion.track_name)  =~ '.*\\\\bthe\\\\b.*'"
        # "RETURN cancion.track_name AS results LIMIT 5"
        # )
        cypher = (
        "MATCH (cancion:Cancion) "
        "WHERE toLower(cancion.track_name) =~ '.*$search_string.*' "
        "RETURN cancion.track_name AS results LIMIT 5 "
        )
        # cypher = (
        # "MATCH (cancion:Cancion) "
        # "WHERE toLower(cancion.track_name)  =~ '.*\\\\ba\\\\b.*' "
        # "RETURN cancion.track_name AS results LIMIT $limit "
        # )
        # cypher = (
        # "MATCH (cancion:Cancion) "
        # "WHERE toLower(cancion.track_name)  =~ '.*\\\\b$search_string\\\\b.*' "
        # "RETURN cancion.track_name AS results LIMIT $limit "
        # )
        print(f"{search_string = }, {limit = }")
        print("cypher = ")
        print(cypher)
        parameters = {
            "search_string": search_string,
            "limit": limit
        }
        final_query = construct_raw_query(cypher, parameters)
        print("final_query = ")
        print(final_query)

        return self.query(final_query, parameters)
