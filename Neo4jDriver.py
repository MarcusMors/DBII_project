
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
            #lista,numero,numero, numero(pero en porcentaje debe ponerse,numero,lista,lista,lista)
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
            #lista,lista(ver el orden),numero(poner como porcentaje),numero,string,string,list,list
    @staticmethod
    def create_user(self, name,correo,contra="123"):
        cypher = """
        CREATE (u:Usuario {nombre: $name, correo: $correo, contraseña: $contra})

        """
        return self.query(cypher, {"name": name, "correo": correo, "contra": contra})
    
    @staticmethod
    def check_use_password(self,usuario,):
        cypher = """
        MATCH (u:Usuario {nombre: $usuario})
        RETURN u.contraseña AS contra

        """
        result= self.query(cypher, {"usuario": usuario})
        contra = result[0]["contra"]
        return contra
    
    @staticmethod
    def get_usuario(self,usuario):
        cypher = """
        MATCH (u:Usuario {nombre: $usuario})-[:AMISTAD]->(amigo)-[:AMISTAD]->(conocido)
        WHERE conocido <> u
        RETURN collect(conocido.nombre) AS conocidos

        """
        result= self.query(cypher, {"usuario": usuario})
        posible_conocido = result[0]["conocidos"]

        cypher = """
        MATCH (u:Usuario {nombre: $usuario})-[:AMISTAD]->(amigo)
        
        RETURN collect(amigo.nombre) AS conocidos

        """
        result= self.query(cypher, {"usuario": usuario})
        amigos = result[0]["conocidos"]
        
        cypher = """
        MATCH (yo:Usuario {nombre: $usuario})-[:AMISTAD]->(amigo:Usuario)-[:CREA]->(lista:Playlist)-[:OBTIENE]->(cancion:Cancion)
        WHERE NOT (yo)-[:CREA]->(:Playlist)-[:OBTIENE]->(cancion)
        RETURN DISTINCT collect(cancion.track_name) AS Cancion
        

        """
        result= self.query(cypher, {"usuario": usuario})
        canciones_amigos = result[0]["Cancion"]

        cypher = """
        MATCH (yo:Usuario {nombre: $usuario})-[:AMISTAD]->(amigo:Usuario)-[:CREA]->(playlist:Playlist)-[:OBTIENE]->(c:Cancion)<-[:CANTA]-(ar:Artista)
        WHERE NOT EXISTS {
            MATCH (yo)-[:CREA]->(:Playlist)-[:OBTIENE]->(c2:Cancion)<-[:CANTA]-(ar)
        }
        
        RETURN DISTINCT collect(ar.nombre) AS artist

        """
        result= self.query(cypher, {"usuario": usuario})
        artistas_amigos = result[0]["artist"]

        cypher = """
        MATCH (u:Usuario {nombre: $usuario})-[:CREA]->(p:Playlist)
        RETURN collect(p.nombre) AS Lista

        """
        result= self.query(cypher, {"usuario": usuario})
        listas = result[0]["Lista"]
        

        return posible_conocido,amigos,canciones_amigos,artistas_amigos,listas
    #lista,lista,lista,lista,lista
    @staticmethod
    def send_request_friend(self,usuario,conocido):
        cypher = """
        MATCH (u1:Usuario {nombre: $usuario})//tu usuario
        MATCH (u2:Usuario {nombre: $conocido})//quien recibe la solicitud
        MERGE (u1)-[:SOLICITUD]->(u2)

        """
        return self.query(cypher, {"usuario": usuario, "conocido": conocido})
      
    @staticmethod
    def denied_request_friend(self,usuario,conocido):
        cypher = """
        MATCH (u1:Usuario {nombre: $usuario})-[r:SOLICITUD]-(u2:Usuario {nombre: $conocido})
        DELETE r

        """
        return self.query(cypher, {"usuario": usuario, "conocido": conocido})

    @staticmethod
    def accept_request_friend(self,usuario,conocido):
        cypher_delete = """
        MATCH (u1:Usuario {nombre: $conocido })-[r:SOLICITUD]-(u2:Usuario {nombre: $usuario})
        DELETE r
        """
        self.query(cypher_delete, {"usuario": usuario, "conocido": conocido})
        
        
        cypher = """
        MATCH (u1:Usuario {nombre: $usuario})
        MATCH (u2:Usuario {nombre: $conocido})
        MERGE (u1)-[:AMISTAD]->(u2)
        MERGE (u2)-[:AMISTAD]->(u1)

        """
        return self.query(cypher, {"usuario": usuario, "conocido": conocido})
    
    @staticmethod
    def get_lista(self,lista):
        cypher = """
        MATCH (u:Usuario)-[:CREA]->(p:Playlist {nombre: $lista})-[:OBTIENE]->(c:Cancion)
        RETURN p.nombre AS Lista, u.nombre AS Creador, collect(c.track_name) AS Canciones

        """
        result= self.query(cypher, {"lista": lista})
        creador = result[0]["Creador"]
        canciones = result[0]["Canciones"]
        
        cypher = """
        MATCH (p:Playlist {nombre: $lista})-[:OBTIENE]->(c1:Cancion)-[:PERTENECE_A]->(g:Genero)
        WITH p, collect(DISTINCT g) AS generosLista
        MATCH (c2:Cancion)-[:PERTENECE_A]->(g2:Genero)
        WHERE NOT (p)-[:OBTIENE]->(c2) AND g2 IN generosLista
        WITH c2, count(DISTINCT g2) AS genero_comun
        ORDER BY genero_comun DESC
        LIMIT 10
        RETURN collect(c2.track_name) AS Cancion
        
        """
        result= self.query(cypher, {"lista": lista})
        canciones_recomendaciones = result[0]["Cancion"]
        return creador,canciones,canciones_recomendaciones
        #string,lista,lista
    @staticmethod
    def create_lista(self,usuario,lista):
        cypher = """
        MATCH (u:Usuario {nombre: $usuario})
        CREATE (p:Playlist {nombre: $lista})
        CREATE (u)-[:CREA]->(p)

        """
        return self.query(cypher, {"usuario":usuario,"lista": lista})
        
    @staticmethod
    def delete_lista(self,lista):
        cypher = """
        MATCH (p:Playlist {nombre: $lista})
        DETACH DELETE p

        """
        return self.query(cypher, {"lista": lista})
    
    @staticmethod
    def agregar_cancion_a_lista(self,lista,cancion):
        cypher = """
        MATCH (p:Playlist {nombre: $lista})
        MATCH (c:Cancion {track_name: $cancion})
        MERGE (p)-[:OBTIENE]->(c)

        """
        return self.query(cypher, {"lista": lista,"cancion":cancion})
    
    @staticmethod
    def eliminar_cancion_a_lista(self,lista,cancion):
        cypher = """
        MATCH (p:Playlist {nombre: $lista})-[r:OBTIENE]->(c:Cancion {track_name: $cancion})
        DELETE r

        """
        return self.query(cypher, {"lista": lista,"cancion":cancion})
    
    @staticmethod
    def mostrar_user(self, usuario):
        cypher = """
        MATCH (u:Usuario {nombre: $usuario})
        RETURN u.nombre AS a, u.contraseña AS b, u.correo AS c

        """

        result= self.query(cypher, {"usuario": usuario})
        record = result[0]
        datos = [record["a"], record["b"], record["c"]]
        return datos
    
    @staticmethod
    def buscar_usuario(self, usuario):
        cypher = """
        MATCH (u:Usuario {nombre: $usuario})
        RETURN u.nombre AS nombre


        """

        result= self.query(cypher, {"usuario": usuario})
        user = result[0]["nombre"]

        return user

    @staticmethod
    def buscar_artista(self, artista):
        cypher = """
        MATCH (u:Artista {nombre: $artista})
        RETURN u.nombre AS nombre
        """

        result= self.query(cypher, {"artista": artista})
        artist = result[0]["nombre"]

        return artist
    
driver=Neo4jDriver()

#print(driver.get_nodes(driver))


#print(driver.get_canciones_de_genero_anime(driver))

#print("///////////////////////")
#print(driver.get_artist(driver,"BTS")[4])
#driver.create_user(driver,"sol","sol@gmail.com")
#print(driver.get_song(driver,"Mikrokosmos")[0])
#print(driver.check_use_password(driver,"sol@gmail.com"))
#print(driver.get_usuario(driver,"Pedro"))
#driver.send_request_friend(driver,"Pedro","sol")
#driver.denied_request_friend(driver,"Pedro","sol")
#driver.accept_request_friend(driver,"Pedro","sol")
#print(driver.get_lista(driver,"Musica3"))
#driver.create_lista(driver,"sol","Musica9")
#driver.delete_lista(driver,"Musica9")
#driver.agregar_cancion_a_lista(driver,"Musica9","Ditto")
#driver.eliminar_cancion_a_lista(driver,"Musica9","Dito")
