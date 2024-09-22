from flask import request, render_template, url_for, redirect, session, make_response
from wishlist_app import app, db, bcrypt
from wishlist_app.models import User, Wish
from wishlist_app.forms import *


def is_login():
    return session.get('auth')


@app.route("/login", methods=['GET', "POST"])
def login():
    mail = request.cookies.get('mail') if request.cookies.get('mail') else ''
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        session['auth'] = True
        session['uemail'] = email
        return redirect(url_for('wishlist_view'))
    return render_template('login.jinja2', mail=mail, form=form)


@app.route("/logout", methods=['GET'])
def logout():
    session['auth'] = None
    return redirect("/")


@app.route("/registrate", methods=['GET', "POST"])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        password1 = form.password1.data
        res = make_response()
        res.set_cookie('mail', email, max_age=60 * 60 * 2)
        pw_hash = bcrypt.generate_password_hash(password1)
        user = User(email=email,
                    name=name,
                    password=pw_hash)
        db.session.add(user)
        db.session.commit()
        session['uemail'] = email
        session['auth'] = True
        return redirect(url_for('wishlist_view'))
    return render_template('registration.jinja2', form=form)

@app.route("/")
@app.route("/my_wishes", methods=['GET', 'POST'])
def wishlist_view():
    if not is_login():
        return redirect(url_for('login'))
    uemail = session['uemail']
    user = User.query.filter(User.email == uemail).first()
    wishes = db.session.query(Wish.id, Wish.name, Wish.price, Wish.url).where(Wish.creator_id == user.id).all()
    return render_template("mywishes.jinja2", wishes=wishes, user=user)


@app.route("/wish/create", methods=['GET', 'POST'])
def wish_create():
    if not is_login():
        return redirect(url_for('login'))
    form = WishCreateForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        price = int(form.price.data)
        url = form.url.data
        user = User.query.filter(User.email == session['uemail']).first()
        creator_id = user.id
        wish = Wish(name=name, creator_id=creator_id, description=description, price=price, url=url)
        db.session.add(wish)
        db.session.commit()
        return redirect(url_for('wishlist_view'))
    return render_template('create.jinja2', form=form)


@app.route("/wish/<int:wish_id>/", methods=['GET', 'POST'])
def detail_view(wish_id):
    wish = db.session.query(Wish.id, Wish.creator_id, Wish.name, Wish.uploaded, Wish.price, Wish.url, Wish.description) \
        .filter(Wish.id == wish_id).first()
    user = User.query.filter(User.email == session['uemail']).first()
    if wish is None:
        return render_template('404.jinja2')
    return render_template('detail.jinja2', wish=wish, user=user)


@app.route("/wish/<int:wish_id>/edit", methods=['GET', 'POST'])
def wish_edit(wish_id):
    if is_login():
        user = User.query.filter(User.email == session['uemail']).first()
        wish = db.session.query(Wish.id, Wish.name, Wish.price, Wish.url, Wish.creator_id, Wish.description
                                ).filter(Wish.id == wish_id).first()
        if user.id == wish.creator_id:
            form = WishEditForm(
                name=wish.name, description=wish.description, url=wish.url, price=wish.price)
            if form.validate_on_submit():
                name = form.name.data
                description = form.description.data
                price = int(form.price.data)
                url = form.url.data
                db.session.query(Wish).filter(Wish.id == wish_id). \
                    update(dict(name=name, description=description, price=price, url=url))
                db.session.commit()
                return redirect(url_for('wishlist_view'))
            return render_template('edit_wish.jinja2', wish=wish, form=form)
        return redirect(url_for('wishlist_view'))
    return redirect(url_for('login'))


@app.route("/wish/<int:wish_id>/delete")
def wish_delete(wish_id):
    if is_login():
        user = User.query.filter(User.email == session['uemail']).first()
        wish = Wish.query.filter(Wish.id == wish_id).first()
        if user.id == wish.creator_id:
            db.session.delete(wish)
            db.session.commit()
            return redirect(url_for('wishlist_view'))
        return redirect(url_for('wishlist_view'))
    return redirect(url_for('login'))