from IsPepsiOkay import app, database, login_manager
from flask import render_template, redirect, request, url_for
from flask.ext.login import LoginManager, current_user, login_required, login_user, logout_user
from forms import LoginForm, RegistrationForm, ChangePasswordForm
import hashlib

@app.route('/')
def index():
    return render_template('index.html')

@login_manager.user_loader
def load_user(user_id):
    return database.get_user(user_id)

#@app.route('/about')
#def about():
#    return render_template('about.html')


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
            user = database.insert_user(form.username.data, form.email.data, m.hexdigest())
            if user is not None:
                login_user(user)
            #flash("Successfully Registered!")
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

