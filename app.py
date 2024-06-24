from flask import Flask, jsonify, render_template, request

from Neo4jDriver import Neo4jDriver
from Queries import Queries

app = Flask(__name__)

# Neo4j connection settings

# # Configurar la conexión a Neo4j

neo4jDriver = Neo4jDriver()

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


@app.route('/query')
def query():
    try:
        nodes = neo4jDriver.get_nodes(neo4jDriver)
        nodes_data = []
        for node in nodes:
            node_data = {"id": node.id, "labels": list(node.labels), "properties": dict(node)}
            nodes_data.append(node_data)
        return jsonify(nodes_data)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.teardown_appcontext
def close_driver(exception):
    neo4jDriver.close()

if __name__ == '__main__':
    # neo4j_session = Neo4jDriver)
    app.run(debug=True)
