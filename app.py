from flask import Flask, jsonify, render_template, request, url_for

from Neo4jDriver import Neo4jDriver
from Queries import Queries

app = Flask(__name__)

# Neo4j connection settings

# # Configurar la conexión a Neo4j

neo4jDriver = Neo4jDriver()

logged_user: bool = True

@app.route('/')
def index_root():
    if logged_user:
        return render_template('index.html')
    else:
        return render_template('login.html')


@app.route('/user/<user_name>')
def show_user_profile(user_name):
    # get user_data
    user = {"username": user_name}
    
    return render_template('user_profile.html',user=user)

@app.route('/signin',methods=["POST","GET"])
def sign_in():
    if request.method == "GET":
        return render_template("signin.html")
    return render_template("signin.html")

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

@app.route('/songs/<song_name>')
def show_song_name(song_name):
    user = {"username": song_name}

    return render_template('songpage.html',user=user)

#### IDK WHAT TO DO WITH THIS
@app.route('/user/<song_name>')
def show_song(song_name):
    user = {"username": song_name}
    
    return render_template('songpage.html',user=user)
#### IDK WHAT TO DO WITH THIS


@app.route('/search', methods=["GET"])
def search():
    search_type = request.args.get('search_type')
    search_text = request.args.get('search_text')

    print(f"{ search_text = }")
    print(f"{ search_type = }")
    records = []

    if search_type == "All":
        pass
    if search_type == "Users":
        records = neo4jDriver.search_artists(neo4jDriver,search_text)
    if search_type == "Playlists":
        records = neo4jDriver.search_playlists(neo4jDriver,search_text)
    if search_type == "Songs":
        records = neo4jDriver.search_songs(neo4jDriver,search_text)
    if search_type == "Producer":
        records = neo4jDriver.search_producer(neo4jDriver,search_text)

    if not records:
        return render_template("partials/no_matches_found.html")

    nodes_data = []
    for r in records:
        print(f"{r = }")
        node_data = {"name": r["results"]}
        nodes_data.append(node_data)

    return render_template("partials/media_section.html",media_infos=nodes_data)
    # return jsonify("hello this is my answer motherfucker")
    # return render_template('songpage.html',user=user)

# @app.route('/user/search')
# def user_search():
#     return render_template('songpage.html',user=user)

# @app.route('/search',methods=["POST"])
@app.route('/song/search',methods=["POST"])
def song_search():
    search_text = request.form.get('search_text')
    print("-----------------------------------")
    print(search_text)
    print("-----------------------------------")
    # search_type = request.form.get('search_type')
    records = neo4jDriver.search_artists(neo4jDriver,search_text)
    nodes_data = []
    for r in records:
        node_data = {"name": r["names"]}
        nodes_data.append(node_data)

    return render_template("search_results.html", names=nodes_data)

# Rutas para cargar dinámicamente el contenido desde Neo4j
@app.route('/featured')
def load_featured():
    # Ejemplo de consulta a Neo4j
    query = "MATCH (s:Song) RETURN s.name LIMIT 5"
    # result = neo4j_session.run_query(query)
    # featured_songs = [record['s.name'] for record in result]
    featured_songs = ["song_1", "song_2", "song_3"]
    return jsonify(items=featured_songs)

featured_songs = [
    {"id": 1, "name": "song_1"},
    {"id": 1, "name": "song_2"},
    {"id": 1, "name": "song_3"},
    {"id": 1, "name": "song_4"},
    {"id": 1, "name": "song_5"},
    {"id": 1, "name": "song_6"},
    {"id": 1, "name": "song_7"},
    {"id": 1, "name": "song_8"},
    ]

@app.route('/friends/recent_likes')
def load_friends_recent_likes():
    # route_function = request.endpoint
    # route_url = url_for(route_function)
    # print(f"{ route_url = }")
    
    # if query is empty, render nothing

    # Ejemplo de consulta a Neo4j
    # return jsonify(items=featured_songs)
    # return render_template("partials/playlists.html", playlists=featured_songs)
    return render_template("partials/media_section.html",media_infos=featured_songs )

@app.route('/myplaylists')
def load_playlists():
    # Ejemplo de consulta a Neo4j
    query = "MATCH (p:Playlist) RETURN p.name LIMIT 5"
    # result = neo4j_session.run_query(query)
    # user_playlists = [record['p.name'] for record in result]
    return render_template("partials/playlists.html", playlists=featured_songs)


@app.route('/home')
def index_home():
    return render_template('index.html')

@app.route('/biblioteca')
def biblioteca():
    return render_template('biblioteca.html')


@app.route('/get/kpop')
def get_kpop():
    names = neo4jDriver.get_canciones_de_genero_kpop(neo4jDriver)
    nodes_data = []
    records = names
    for r in records:
        node_data = {"name": r["names"]}
        nodes_data.append(node_data)

    return render_template("partials/media_section.html", media_infos=nodes_data)

@app.route('/get/anime')
def get_anime():
    names = neo4jDriver.get_canciones_de_genero_anime(neo4jDriver)
    nodes_data = []
    records = names
    for r in records:
        node_data = {"name": r["names"]}
        nodes_data.append(node_data)

    return render_template("partials/media_section.html", media_infos=nodes_data)


@app.route('/query')
def query():
    # int(request.args.get("page", 1)) # default a 1 si no hay arg page
    try:
        nodes = neo4jDriver.get_nodes(neo4jDriver)
        nodes_data = []
        for node in nodes:
            node_data = {"id": node.id, "labels": list(node.labels), "properties": dict(node)}
            nodes_data.append(node_data)
        return render_template('biblioteca.html')
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500



################################################################################
#  Error handling
################################################################################
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.teardown_appcontext
def close_driver(exception):
    neo4jDriver.close()


################################################################################
#  Testing cosas
################################################################################

@app.route('/layout')
def app_layout():
    return render_template('app_layout.html')


if __name__ == '__main__':
    # neo4j_session = Neo4jDriver)
    app.run(debug=True,port=5001)
