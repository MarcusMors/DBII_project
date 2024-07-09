from flask import Flask, jsonify, render_template, request, url_for, redirect, session

from Neo4jDriver import Neo4jDriver
from Queries import Queries

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 

# Neo4j connection settings
neo4jDriver = Neo4jDriver()

# Datos simulados de usuarios registrados
emails = ["alivezeh@gmail.com", "jose.vilca.campana@ucsp.edu.pe", "a@gmail.com"]
usernames = ["alivezeh", "marcusmors", "tujfa"]

# Variable para manejar sesión de usuario
logged_user = False

# Routes

# Página principal
@app.route('/')
def index_root():
    if logged_user:
        return render_template('index.html')
    else:
        return render_template('signin.html')


@app.route('/user_profile')
def show_user_profile():
    # Obtener el nombre de usuario desde la sesión
    username = session.get('username')
    perfil = neo4jDriver.mostrar_user(neo4jDriver,username)
    # Simular datos de usuario
    user_data = {
        'username': perfil[0],
        'nombre': perfil[1],
        'email': perfil[2],
    }    
    print(user_data)

    return render_template('user_profile.html', user=user_data)




@app.route('/signin', methods=["POST", "GET"])
def sign_in():
    global logged_user
        
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        perfil = neo4jDriver.check_use_password(neo4jDriver,username)
        # Verificar las credenciales (aquí deberías tener tu lógica de autenticación)
        if perfil == password:
            session['username'] = username
            logged_user = True
            return redirect(url_for('index_root'))
        else:
            return render_template('signin.html', message='Credenciales incorrectas. Inténtalo de nuevo.')

    return render_template("signin.html")


@app.route('/signout')
def sign_out():
    global logged_user
    session.pop('username', None)
    logged_user = False
    return redirect(url_for('sign_in'))


@app.route('/signup', methods=["POST", "GET"])
def signup():
    
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Verificar si el nombre de usuario o el correo electrónico ya están registrados
        if username in usernames:
            message = f"El nombre de usuario '{username}' ya está en uso. Por favor, elige otro."
            return render_template('signup.html', message=message)
        elif email in emails:
            message = f"El correo electrónico '{email}' ya está registrado."
            return render_template('signup.html', message=message)
        else:
            # Agregar usuario registrado (simulado)
            usernames.append(username)
            emails.append(email)
            session['username'] = username  # Establecer la sesión después del registro
            logged_user = True
            neo4jDriver.create_user(neo4jDriver,username, email, password)
            return redirect(url_for('index_root'))  # Redirigir a la página principal después del registro            
       
    return render_template('signup.html')


@app.route('/validate/email', methods=["POST"])
def validate_email():
    email = request.form.get("email")
    if email in emails:
        return "This email has been already taken."
    else:
        return ""


@app.route('/validate/username', methods=["POST"])
def validate_username():
    username = request.form.get("username")
    if username in usernames:
        return "This username has been already taken."
    else:
        return ""

users = {    "test@example.com": "password123"}##
@app.route('/login', methods=['GET', 'POST'])##
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if email in users and users[email] == password:
            flash('ingreso exitoso', 'success')
            return redirect(url_for('index_root'))
        else:
            flash('email o pasword incorrecto. Vuelva a revisar', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')



@app.route('/songs/<song_name>')
def show_song_name(song_name):
    song_raw = neo4jDriver.get_song(neo4jDriver, song_name)
    print(f"{ song_raw = }")
    song = {
        "genre":song_raw[0],
        "data":{
            "name": song_raw[1][0],
            "top_streak": song_raw[1][1],
            "reproducciones": song_raw[1][2],
            "duration_ms": song_raw[1][3],
            "date": song_raw[1][4],
        },
        "danceability": song_raw[2], # danceability (0-100) # 60% de las personas bailan esta cancion
        "top_rank":song_raw[3],
        "authors":song_raw[4],
        "producer":song_raw[5],
        "appears_in_playlists":song_raw[6], # lista Playlists con esa canción
        "related_songs":song_raw[7],
    }
    return render_template('songpage.html', song=song)


@app.route('/user/<username>')
def show_song(username):
    records = neo4jDriver.buscar_usuario(neo4jDriver,username)

    nodes_data = []
    for r in records:
        node_data = {"name": r["results"]}
        nodes_data.append(node_data)

    if len(nodes_data) == 0:
        return render_template("errors/404.html")

    return render_template('user_profile.html', user=user)

# @app.route('/search')
@app.route('/search', methods=["GET"])
def search():
    search_query = request.args.get('search_query')
    # trigger= request.headers.get("HX-Trigger")
    target= request.headers.get("HX-Target")
    search_type = request.args.get("search_type")

    print(f"{ search_type = }")
    print(f"{ search_query = }")
    print(f"{ target = }")
    records = []

    if search_type == "All":
        pass
    if search_type == "Users":
        if search_query == "__conocidos":
            username = session.get("username")
            records = neo4jDriver.get_usuario(neo4jDriver,username)
            nodes_data = []
            for r in records:
                node_data = {"name": r["results"]}
                nodes_data.append(node_data)
            return render_template("partials/user_section.html",media_infos=nodes_data)
        else:
            records = neo4jDriver.buscar_usuario(neo4jDriver,search_query)
    if search_type == "Artists":
        records = neo4jDriver.buscar_artists(neo4jDriver,search_query)
    if search_type == "Playlists":
        records = neo4jDriver.search_playlists(neo4jDriver,search_query)
    if search_type == "Songs":
        records = neo4jDriver.search_songs(neo4jDriver,search_query)
    if search_type == "Producer":
        records = neo4jDriver.search_producer(neo4jDriver,search_query)

    nodes_data = []
    for r in records:
        node_data = {"name": r["results"]}
        nodes_data.append(node_data)

    if len(nodes_data) == 0:
        print("NO MATCHES")
        return render_template("partials/no_matches_found.html")

    if target == "search_table":
        print("HX-Target")
        print(f"{ nodes_data = }")
        return render_template("partials/search_rows.html", media_infos=nodes_data)

    return render_template("partials/media_section.html",media_infos=nodes_data, prefix=search_type)
    # return jsonify("hello this is my answer motherfucker")
    # return render_template('songpage.html',user=user)


@app.route('/song/search', methods=["POST"])
def song_search():
    search_query = request.form.get('search_query')
    print("-----------------------------------")
    print(search_query)
    print("-----------------------------------")
    # search_type = request.form.get('search_type')
    records = neo4jDriver.search_artists(neo4jDriver,search_query)
    nodes_data = []
    for r in records:
        node_data = {"name": r["names"]}
        nodes_data.append(node_data)

    return render_template("search_results.html", names=nodes_data)


    featured_songs = ["song_1", "song_2", "song_3"]
@app.route('/featured')
def load_featured():
    return jsonify(items=featured_songs)


@app.route('/friends/recent_likes')
def load_friends_recent_likes():
    return render_template("partials/media_section.html", media_infos=featured_songs, prefix="song")


# Ruta para cargar la página playlists.html
@app.route('/playlists')
def load_playlists():
    # Aquí podrías agregar lógica para obtener datos de playlists si es necesario
    playlists_data = [
        {'name': 'Playlist 1', 'songs': ['Song A', 'Song B', 'Song C']},
        {'name': 'Playlist 2', 'songs': ['Song X', 'Song Y', 'Song Z']}
        # Agrega más datos según sea necesario
    ]
    return render_template('playlists.html', playlists=playlists_data)

# Otras rutas y lógica de tu aplicación



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

    return render_template("partials/media_section.html", media_infos=nodes_data, prefix="song")


@app.route('/get/anime')
def get_anime():
    names = neo4jDriver.get_canciones_de_genero_anime(neo4jDriver)
    nodes_data = []
    records = names
    for r in records:
        node_data = {"name": r["names"]}
        nodes_data.append(node_data)

    return render_template("partials/media_section.html", media_infos=nodes_data, prefix="song")


@app.route('/query')
def query():
    try:
        nodes = neo4jDriver.get_nodes(neo4jDriver)
        nodes_data = []
        for node in nodes:
            node_data = {"id": node.id, "labels": list(node.labels), "properties": dict(node)}
            nodes_data.append(node_data)
        return render_template('biblioteca.html')

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Manejo de errores

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


# Cerrar conexión Neo4j al finalizar la aplicación

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
    app.run(debug=True, port=5001)