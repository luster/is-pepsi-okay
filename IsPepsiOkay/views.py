from IsPepsiOkay import app, database, login_manager
from flask import render_template, redirect, request, url_for
from flask.ext.login import LoginManager, current_user, login_required, login_user, logout_user
from forms import LoginForm, RegistrationForm, ChangePasswordForm
from models import Tmp
import hashlib
import json


@app.route('/')
def index():
    print database.get_user(username=current_user.get_id()).uid
    return render_template('index.html')


@app.route('/about')
def about():
    return 'About Page TODO'


@login_manager.user_loader
def load_user(user_id):
    return database.get_user(user_id)


@app.route("/recommendations")
def recommendations():
    uid = current_user.get_id()
    if not uid:
        return redirect("/accounts/login")

    return render_template('recommendations.html')


@app.route("/search/autocomplete/movies")
def search_movie():
    title = request.args.get('title')
    if not title:
        return '{}'
    return database.get_movies_like(title, 10)


@app.route("/search/autocomplete/people")
def search_people():
    person = request.args.get('title')
    if not person:
        return '{}'
    return database.get_people_like(person, 10)


def get_movies(mid):
    if not mid:
        return None
    movie = database.get_movie_by_id(mid)
    if not movie:
        return None
    people = database.get_people_from_movie(mid)
    genres = database.get_genre(mid)
    for person in people:
        credits = database.get_movie_credits_by_person(movie.mid, person.pid)
        if credits.directed:
            movie.directors.append(person)
        if credits.produced:
            movie.producers.append(person)
        if credits.wrote:
            movie.writers.append(person)
        if credits.composed:
            movie.composers.append(person)
        if credits.acted:
            movie.actors.append(person)
    movie.genres = genres
    return movie


@app.route("/api/movies/<mid>")
def movie_api(mid):
    m = get_movies(mid)
    if not m:
        return '{}'
    return m.to_json()


@app.route("/movies/<mid>")
def render_movie(mid):
    m = get_movies(mid)
    error = None
    if not m:
        error = "Sorry, movie does not exist!"
    return render_template("movie.html", movie=m, error=error)


@app.route("/api/genres/<gid>")
def genre_api(gid):
    mids = database.get_movies_by_genre(gid)
    if not mids:
        return '{}'
    movies = []
    for mid in mids:
        movies.append(get_movies(mid))
    t = Tmp()
    t.movies = movies
    return t.to_json()


@app.route("/genres/<gid>")
def genre_page(gid):
    g = database.get_genre_name(gid)
    m = database.get_movies_by_genre(gid)
    movies = []
    for mid in m:
        movies.append(get_movies(mid))
    error = None
    if not g:
        error = "Sorry, genre does not exist!"
    if not m:
        error = "Sorry, genre does not exist!"
    return render_template("genre.html", movies=movies, genre=g, error=error)


@app.route("/people/<pid>")
def person_page(pid):
    p = database.get_person_name(pid)
    m = database.get_movies_by_person(pid)
    error = None
    if not p:
        error = "Sorry, person does not exist!"
    if not m:
        error = "Sorry, person does not exist!"
    return render_template("person.html", movies=m, person=p, error=error)


@app.route("/rate/<otype>/<oid>", methods=["GET", "POST"])
def rate(otype, oid):
    rating = 0
    t_map = {
        'movies': 'Has_Watched',
        'people': 'Likes_Person',
        'genres': 'Likes_Genre'
    }
    if request.method == 'GET':
        otypes = ['movies', 'people', 'genres']
        if otype not in otypes:
            return '0'

        pkey_name = otype[0] + 'id'

        uid = database.get_user(username=current_user.get_id()).uid

        table = t_map[otype]
        checked, rating = database.get_rating(table, uid, pkey_name, oid)

        r = {'checked': checked, 'rating': rating}
        return json.dumps(r)


    if request.method == 'POST':
        # otype: movies, people, genres
        # oid: primary key for object type
        # glike, plike, urating
        rating = float(request.json.get('rating', 0))
        if not current_user.is_authenticated():
            return '0'
        uid = database.get_user(username=current_user.get_id()).uid
        otypes = ['movies', 'people', 'genres']
        if otype not in otypes:
            return '0'
        pkey_name = otype[0] + 'id'; # mid, pid, gid
        table = t_map[otype]
        success = database.rate(table, uid, pkey_name, oid, rating)

        return str(rating)


@app.route("/accounts/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = False
    if request.method == 'POST' and form.validate():
        m = hashlib.md5()
        m.update(form.password.data)
        user = database.get_user(username=form.username.data, password=m.hexdigest())
        if user is not None:
            login_user(user)
            return redirect(request.args.get("next") or url_for("index"))
        else:
            error=True
    return render_template("accounts/login.html", form=form, error=error)


@app.route("/accounts/logout")
@login_required
def logout():
    logout_user()
    return redirect(request.args.get("next") or url_for("index"))


@app.route("/accounts/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    username_error = False
    if request.method == 'POST' and form.validate():
        try:
            m = hashlib.md5()
            m.update(form.password.data)
            user = database.insert_user(form.username.data, form.email.data, m.hexdigest(), form.dob)
            if user is not None:
                login_user(user)
            return redirect(request.args.get("next") or url_for("index"))
        except Exception:
            username_error = True
    return render_template("accounts/register.html", form=form, username_error=username_error)


@app.route("/accounts/password/change", methods=["GET", "POST"])
@login_required
def change_pass():
    form = ChangePassForm()
    error = False
    if request.method == 'POST' and form.validate():
        m = hashlib.md5()
        m.update(form.old_password.data)
        user = database.get_user(username=current_user.username, password=m.hexdigest())
        if user is not None:
            m = hashlib.md5()
            m.update(form.password.data)
            user = database.update_user(username=current_user.username, password=m.hexdigest())
            return redirect(url_for("change_pass_success"))
        error = True
    return render_template("accounts/password_change_form.html", form=form, error=error)


@app.route("/accounts/password/change/success")
def change_pass_success():
    return render_template("accounts/password_change_done.html")


@app.route("/accounts/email/change", methods=["GET", "POST"])
@login_required
def change_email():
    success = False
    if request.method == 'POST' and request.form['email']:
        user = database.update_user(username=current_user.username, email=request.form['email'])
        success = True
        user = database.get_user(username=current_user.username)
        if user is not None:
            login_user(user)
    return render_template("accounts/change_email.html", success=success)


@app.route("/accounts/delete", methods=["GET", "POST"])
@login_required
def delete_account():
    success = True
    user = database.update_user(username=current_user.username, is_active=False)
    logout_user()
    return render_template("accounts/delete.html", success=success)


