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

        # Verificar las credenciales (aquí deberías tener tu lógica de autenticación)
        if username in usernames and password == '1234':
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
    user = {"username": song_name}
    return render_template('songpage.html', user=user)


@app.route('/user/<song_name>')
def show_song(song_name):
    user = {"username": song_name}
    return render_template('songpage.html', user=user)

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
        records = neo4jDriver.search_artists(neo4jDriver,search_query)
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

    return render_template("partials/media_section.html",media_infos=nodes_data)
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


@app.route('/featured')
def load_featured():
    featured_songs = ["song_1", "song_2", "song_3"]
    return jsonify(items=featured_songs)


@app.route('/friends/recent_likes')
def load_friends_recent_likes():
    return render_template("partials/media_section.html", media_infos=featured_songs)


@app.route('/myplaylists')
def load_playlists():
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
