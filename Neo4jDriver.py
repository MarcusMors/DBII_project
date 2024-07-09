
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
            "MATCH (c:Cancion)-[:PERTENECE_A]->(g1:Genero {nombre: 'anime'});"
            "RETURN c.track_name AS names LIMIT 5;"
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

#DESDE AQUI SON LAS DEFINICIONES QUE REALIZE SI SON DE AYUDA
    @staticmethod
    def get_artist(self, artist_string):
        cypher = """
        MATCH (artista:Artista {nombre: $artist_string})
        MATCH (artista)-[:CANTA]->(cancion:Cancion)
        RETURN  collect(cancion.track_name) AS Canciones
        """
        result= self.query(cypher, {"artist_string": artist_string})
        canciones = result[0]["Canciones"]
        cypher = """
        MATCH (a:Artista {nombre: $artist_string})-[:CANTA]->(c:Cancion)-[:PERTENECE_A]->(g:Genero)
        RETURN collect(DISTINCT g.nombre) AS Generos
        """
        result= self.query(cypher, {"artist_string": artist_string})
        generos = result[0]["Generos"]
        
        cypher = """
        MATCH (a:Artista {nombre: $artist_string})-[:CANTA]->(c:Cancion)<-[:PRODUCE]-(p:Productora)
        RETURN collect(DISTINCT p.nombre) AS Productoras
        """
        result= self.query(cypher, {"artist_string": artist_string})
        productoras = result[0]["Productoras"]

        cypher = """
        MATCH (a:Artista {nombre: $artist_string})-[:CANTA]->(c:Cancion)
        RETURN  toInteger(sum(c.duration_ms) / 60000) AS TotalDurationInMinutes
        """
        result= self.query(cypher, {"artist_string": artist_string})
        minutos = result[0]["TotalDurationInMinutes"]

        cypher = """
        MATCH (a:Artista {nombre: $artist_string})-[:CANTA]->(c:Cancion)<-[:BAILAN]-(b:Baile)
        RETURN  avg(b.danceability)*100 AS PromedioBaile
        """
        result= self.query(cypher, {"artist_string": artist_string})
        baile = int(result[0]["PromedioBaile"])

        cypher = """
        MATCH (a:Artista {nombre: $artist_string})-[:CANTA]->(c:Cancion)<-[:LLEGA]-(p:Popularidad)
        WITH a, min(p.peak_rank) AS PopularidadTop
        RETURN  PopularidadTop

        """
        result= self.query(cypher, {"artist_string": artist_string})
        top_rank = result[0]["PopularidadTop"]

        cypher = """
        MATCH (a:Artista {nombre: $artist_string})-[:CANTA]->(c:Cancion)
        RETURN  sum(c.streams) AS TotalReproducciones

        """
        result= self.query(cypher, {"artist_string": artist_string})
        reproducciones = result[0]["TotalReproducciones"]

        cypher = """
        MATCH (a:Artista {nombre: $artist_string})-[:CANTA]->(c:Cancion)<-[:CANTA]-(otro:Artista)
        RETURN collect(otro.nombre) AS Colabora

        """
        result= self.query(cypher, {"artist_string": artist_string})
        artistas_collab = result[0]["Colabora"]
        #print(artistas_collab)
        return productoras, top_rank,reproducciones,baile,minutos,artistas_collab, generos,canciones
    
    @staticmethod
    def get_song(self, song_string):
        cypher = """
        MATCH (c:Cancion {track_name: $song_string})-[:PERTENECE_A]->(g:Genero)
        RETURN  collect(g.nombre) AS Generos

        """
        result= self.query(cypher, {"song_string": song_string})
        generos = result[0]["Generos"]

        cypher = """
        
        MATCH (c:Cancion {track_name: $song_string})
        RETURN c.track_name AS a,
            c.days_on_chart AS b,
            c.streams AS c,
            c.duration_ms AS d,
            c.date AS e

        """
        result= self.query(cypher, {"song_string": song_string})
        record = result[0]
        datos = [record["a"], record["b"], record["c"], record["d"], record["e"]]


        cypher = """
        MATCH (c:Cancion {track_name: $song_string})<-[:BAILAN]-(b:Baile)
        RETURN  b.danceability*100 AS Danceability

        """
        result= self.query(cypher, {"song_string": song_string})
        baile = int(result[0]["Danceability"])
        
        cypher = """
        MATCH (c:Cancion {track_name: $song_string})<-[:LLEGA]-(p:Popularidad)
        RETURN  p.peak_rank AS Popularidad

        """
        result= self.query(cypher, {"song_string": song_string})
        top_rank = int(result[0]["Popularidad"])
        
        cypher = """
        MATCH (a:Artista)-[:CANTA]->(c:Cancion {track_name: $song_string})
        RETURN collect(a.nombre) AS Artista

        """
        result= self.query(cypher, {"song_string": song_string})
        artista = result[0]["Artista"]
        
        cypher = """
        MATCH (a:Productora)-[:PRODUCE]->(c:Cancion {track_name: $song_string})
        RETURN a.nombre AS Productora

        """
        result= self.query(cypher, {"song_string": song_string})
        productora = result[0]["Productora"]

        cypher = """
       MATCH (p:Playlist)-[:OBTIENE]->(c:Cancion {track_name: $song_string})
        RETURN collect(p.nombre) AS Playlist

        """
        result= self.query(cypher, {"song_string": song_string})
        playlists = result[0]["Playlist"]

        cypher = """
        MATCH (cancion:Cancion {track_name:  $song_string})-[:PERTENECE_A]->(genero:Genero)
        MATCH (otraCancion:Cancion)-[:PERTENECE_A]->(genero)
        WHERE cancion <> otraCancion
        WITH otraCancion
        ORDER BY otraCancion.track_name
        LIMIT 15
        RETURN collect(otraCancion.track_name) AS CancionRelacionada

        """
        result= self.query(cypher, {"song_string": song_string})
        cancion_relacionada = result[0]["CancionRelacionada"]

        return generos,datos,baile,top_rank,artista,productora,playlists,cancion_relacionada

    @staticmethod
    def create_user(self, name,correo,contra="123"):
        cypher = """
        CREATE (u:Usuario {nombre: $name, correo: $correo, contraseña: $contra})

        """
        return self.query(cypher, {"name": name, "correo": correo, "contra": contra})
    
    @staticmethod
    def check_use_password(self,correo,):
        cypher = """
        MATCH (u:Usuario {correo: $correo})
        RETURN u.contraseña AS contra

        """
        result= self.query(cypher, {"correo": correo})
        contra = result[0]["contra"]
        return contra



