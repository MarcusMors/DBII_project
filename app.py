from flask import Flask, jsonify, render_template
from neo4j import GraphDatabase

app = Flask(__name__)

# Configurar la conexión a Neo4j
uri = "bolt://localhost:7687"  # Cambia localhost por la dirección de tu servidor Neo4j
user = "neo4j"
password = "tu_contraseña"

# Clase de utilidad para manejar la sesión de Neo4j
# class Neo4jSession:
#     def __init__(self, uri, user, password):
#         self._driver = GraphDatabase.driver(uri, auth=(user, password))

#     def close(self):
#         self._driver.close()

#     def run_query(self, query):
#         with self._driver.session() as session:
#             result = session.run(query)
#             return [record for record in result]


@app.route('/user/<user_name>')
def show_user_profile(user_name):
    # get user_data
    user = {"username": user_name}
    
    return render_template('userpage.html',user=user)

@app.route('/user/<song_name>')
def show_user_profile(song_name):
    user = {"username": song_name}
    
    return render_template('songpage.html',user=user)


# Rutas para cargar dinámicamente el contenido desde Neo4j
@app.route('/featured')
def load_featured():
    # Ejemplo de consulta a Neo4j
    query = "MATCH (s:Song) RETURN s.name LIMIT 5"
    # result = neo4j_session.run_query(query)
    # featured_songs = [record['s.name'] for record in result]
    featured_songs = ["song_1", "song_2", "song_3"]
    return jsonify(items=featured_songs)

@app.route('/myplaylists')
def load_playlists():
    # Ejemplo de consulta a Neo4j
    query = "MATCH (p:Playlist) RETURN p.name LIMIT 5"
    # result = neo4j_session.run_query(query)
    # user_playlists = [record['p.name'] for record in result]
    return jsonify(items=user_playlists)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/biblioteca')
def biblioteca():
    return render_template('biblioteca.html')

if __name__ == '__main__':
    # neo4j_session = Neo4jSession(uri, user, password)
    app.run(debug=True)
