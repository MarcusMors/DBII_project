from flask import Blueprint, Flask, jsonify, render_template, request
from neo4j import GraphDatabase

app = Flask(__name__)
# main = Blueprint("main", __name__)

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
    
    return render_template('user_profile.html',user=user)

@app.route('/signup',methods=["POST"])
def signup_new_user():
    print("new submission")
    return ""

@app.route('/signup')
def signup():
    return render_template('signup.html')
# <!-- {{ contact.errors['email'] }} -->

emails = ["alivezeh@gmail.com", "jose.vilca.campana@ucsp.edu.pe", "a@gmail.com"]

@app.route('/validate/email', methods=["POST"])
def validate_email():
    print("here")
    email = request.form.get("email")
    if email in emails:
        return "This email has been already taken."
    else:
        return ""

usernames = ["alivezeh", "marcusmors", "tujfa"]

@app.route('/validate/username', methods=["POST"])
def validate_username():
    print("here")
    username = request.form.get("username")
    if username in usernames:
        return "This username has been already taken."
    else:
        return ""


#### IDK WHAT TO DO WITH THIS
@app.route('/user/<song_name>')
def show_song(song_name):
    user = {"username": song_name}
    
    return render_template('songpage.html',user=user)
#### IDK WHAT TO DO WITH THIS


@app.route('/user/search')
def search():
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

@app.route('/friends/recent_likes')
def load_friends_recent_likes():
    # Ejemplo de consulta a Neo4j
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


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if __name__ == '__main__':
    # neo4j_session = Neo4jSession(uri, user, password)
    app.run(debug=True)
