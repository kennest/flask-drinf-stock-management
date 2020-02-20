from flask import render_template, url_for, redirect, flash, request, jsonify
from flaskinventory import app, db, login_manager, login_required, bcrypt,current_user, login_user,logout_user
from flaskinventory.forms import addproduct, addlocation, moveproduct, editproduct, editlocation, sellproduct, \
    addperson, editperson, editsellproduct, editmoveproduct, LoginForm, RegistrationForm
from flaskinventory.models import Location, Product, Movement, Balance, Person, Sell, Stock, User
import time, datetime
from sqlalchemy.exc import IntegrityError

@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id)


@app.route("/Overview")
@app.route("/")
@login_required
def overview():
    main_exist = Person.query.filter_by(name="CL_001").first()
    if not main_exist:
        main = Person(name="CL_001", phone="00000000", lastname="CL_OO1", code="CL_001")
        db.session.add(main)
        db.session.commit()

    cave_exist = Location.query.filter_by(loc_name="Cave").first()
    if not cave_exist:
        cave = Location(loc_name="Cave")
        db.session.add(cave)
        db.session.commit()

    bar_exist = Location.query.filter_by(loc_name="Bar").first()
    if not bar_exist:
        bar = Location(loc_name="Bar")
        db.session.add(bar)
        db.session.commit()

    balance = Balance.query.all()
    exists = bool(Balance.query.all())
    if not exists:
        flash(f'Add products,locations and make transfers to view', 'info')
    return render_template('overview.html', balance=balance)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('overview'))
        else:
            flash('Login Unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('overview'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your Account has been created', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/Product", methods=['GET', 'POST'])
@login_required
def product():
    form = addproduct()
    eform = editproduct()
    details = Product.query.all()

    exists = bool(Product.query.all())
    if exists == False and request.method == 'GET':
        flash(f'Add products to view', 'info')
    elif eform.validate_on_submit() and request.method == 'POST':

        p_id = request.form.get("productid", "")
        pname = request.form.get("productname", "")
        details = Product.query.all()
        prod = Product.query.filter_by(id=p_id).first()
        prod.prod_name = eform.editname.data
        Balance.query.filter_by(product=pname).update(dict(product=eform.editname.data))
        Movement.query.filter_by(pname=pname).update(dict(pname=eform.editname.data))
        try:
            db.session.commit()
            flash(f'Your product  has been updated!', 'success')
            return redirect('/Product')
        except IntegrityError:
            db.session.rollback()
            flash(f'This product already exists', 'danger')
            return redirect('/Product')
        return render_template('product.html', title='Products', details=details, eform=eform)

    elif form.validate_on_submit():
        main = Location.query.filter_by(loc_name="Principal").first()
        product = Product(prod_name=form.prodname.data)
        db.session.add(product)
        try:
            db.session.commit()
            flash(f'Your product {form.prodname.data} has been added!', 'success')
            return redirect(url_for('product'))
        except IntegrityError:
            db.session.rollback()
            flash(f'This product already exists', 'danger')
            return redirect('/Product')
    return render_template('product.html', title='Products', eform=eform, form=form, details=details)


@app.route("/Person", methods=['GET', 'POST'])
@login_required
def person():
    form = addperson()
    eform = editperson()
    persons = Person.query.all()
    exists = bool(Person.query.all())
    if exists == False and request.method == 'GET':
        flash(f'Add Person to view', 'info')
    elif eform.validate_on_submit() and request.method == 'POST':

        p_id = request.form.get("personid", "")
        print("Person ID =>", p_id)
        p_name = request.form.get("personname", "")
        p_lastname = request.form.get("personlastname", "")
        p_code = request.form.get("personcode", "")
        p_phone = request.form.get("personphone", "")
        person = Person.query.filter_by(id=p_id).first()
        person.name = eform.editpersonname.data
        person.lastname = eform.editpersonlastname.data
        person.phone = eform.editpersonphone.data
        person.code = eform.editpersoncode.data
        Person.query.filter_by(id=p_id).update(dict(product=eform.editname.data))
        try:
            db.session.commit()
            flash(f'Your person  has been updated!', 'success')
            return redirect('/Person')
        except IntegrityError:
            db.session.rollback()
            flash(f'This Person already exists', 'danger')
            return redirect('/Person')
        return render_template('person.html', title='Person', persons=persons, eform=eform)

    elif form.validate_on_submit():
        person = Person(name=form.personname.data, lastname=form.personlastname.data, phone=form.personphone.data,
                        code=form.personcode.data)
        db.session.add(person)
        try:
            db.session.commit()
            flash(f'Your Person {form.personname.data} has been added!', 'success')
            return redirect(url_for('person'))
        except IntegrityError:
            db.session.rollback()
            flash(f'This Person already exists', 'danger')
            return redirect('/Person')
    return render_template('person.html', title='Products', eform=eform, form=form, persons=persons)


@app.route("/Location", methods=['GET', 'POST'])
@login_required
def loc():
    form = addlocation()
    lform = editlocation()
    details = Location.query.all()
    exists = bool(Location.query.all())
    if exists == False and request.method == 'GET':
        flash(f'Add locations  to view', 'info')
    if lform.validate_on_submit() and request.method == 'POST':
        p_id = request.form.get("locid", "")
        locname = request.form.get("locname", "")
        details = Location.query.all()
        loc = Location.query.filter_by(loc_id=p_id).first()
        loc.loc_name = lform.editlocname.data
        Balance.query.filter_by(location=locname).update(dict(location=lform.editlocname.data))
        Movement.query.filter_by(frm=locname).update(dict(frm=lform.editlocname.data))
        Movement.query.filter_by(to=locname).update(dict(to=lform.editlocname.data))
        try:
            db.session.commit()
            flash(f'Your location  has been updated!', 'success')
            return redirect(url_for('loc'))
        except IntegrityError:
            db.session.rollback()
            flash(f'This location already exists', 'danger')
            return redirect('/Location')
    elif form.validate_on_submit():
        loc = Location(loc_name=form.locname.data)
        db.session.add(loc)
        try:
            db.session.commit()
            flash(f'Your location {form.locname.data} has been added!', 'success')
            return redirect(url_for('loc'))
        except IntegrityError:
            db.session.rollback()
            flash(f'This location already exists', 'danger')
            return redirect('/Location')
    return render_template('loc.html', title='Locations', lform=lform, form=form, details=details)


@app.route("/Sell", methods=['GET', 'POST'])
@login_required
def sell():
    form = sellproduct()
    eform = editsellproduct()
    sells = Sell.query.all()
    exists = bool(Sell.query.all())
    if exists == False and request.method == 'GET':
        flash(f'Sell of products  to view', 'info')
    # ----------------------------------------------------------

    person_choices = Person.query.with_entities(Person.id, Person.name).all()
    stocks = Stock.query.all()
    prod_choices = []
    for n in stocks:
        t = (n.id, n.product.prod_name + " ----->> " + n.location.loc_name + " (" + str(n.price) + " F CFA)")
        prod_choices.append(t)
    prod_list_names = []
    person_list_names = []
    prod_list_names += prod_choices
    person_list_names += person_choices
    # passing list_names to the form for select field
    form.product.choices = prod_list_names
    form.person.choices = person_list_names
    # --------------------------------------------------------------
    # send to db
    if form.is_submitted() and request.method == 'POST':
        print("Form Person=>", form.person.data)
        timestamp = datetime.datetime.now()
        prod_stocks = Stock.query.filter_by(id=form.product.data).all()
        prod_av_qte = 0
        for n in prod_stocks:
            prod_av_qte = prod_av_qte + n.prod_qty

        print("Qte Available",prod_av_qte)
        print("Qte Incoming",form.prodqty.data)
        if form.prodqty.data<=prod_av_qte :
            sell = Sell(date=timestamp, person_id=form.person.data,
                        qty=form.prodqty.data, credit=form.credit.data, stock_id=form.product.data)
            db.session.add(sell)
            db.session.commit()
            flash(f'Your Sell has been added!', 'success')
        else:
            flash(f'Erreur! la quantité est trop élèvée par rapport au stock', 'error')
        return redirect(url_for('sell'))
    return render_template('sell.html', title='Sells', form=form, sells=sells, eform=eform)


@app.route("/Reception", methods=['GET', 'POST'])
@login_required
def reception():
    form = moveproduct()
    eform = editmoveproduct()
    stocks = Stock.query.all()
    exists = bool(Stock.query.all())
    if exists == False and request.method == 'GET':
        flash(f'Transfer products  to view', 'info')
    # ----------------------------------------------------------
    prod_choices = Product.query.with_entities(Product.id, Product.prod_name).all()
    loc_choices = Location.query.with_entities(Location.id, Location.loc_name).all()
    prod_list_names = []
    dest_list_names = []
    prod_list_names += prod_choices
    dest_list_names += loc_choices
    # passing list_names to the form for select field
    form.mprodname.choices = prod_list_names
    form.destination.choices = dest_list_names
    # --------------------------------------------------------------
    # send to db
    if form.is_submitted() and request.method == 'POST':
        print("Reception data=>", form.price_unit.data)
        timestamp = datetime.datetime.now()
        stock = Stock(created_at=timestamp, price=form.price_unit.data, loc_id=form.destination.data,
                      product_id=form.mprodname.data, prod_qty=form.mprodqty.data)
        db.session.add(stock)
        db.session.commit()
        flash(f'Your Stock has been added!', 'success')
        return redirect(url_for('reception'))
    return render_template('reception.html', title='Receptions', form=form, eform=eform, stocks=stocks)


def check(to, name, qty):
    prodq = Product.query.filter_by(prod_name=name).first()
    if prodq.prod_qty >= qty:
        prodq.prod_qty -= qty
        bal = Balance.query.filter_by(location=to, product=name).first()
        a = str(bal)
        if (a == 'None'):
            new = Balance(product=name, location=to, quantity=qty)
            db.session.add(new)
        else:
            bal.quantity += qty
        db.session.commit()
    else:
        return False


@app.route("/delete")
@login_required
def delete():
    type = request.args.get('type')
    if type == 'product':
        pid = request.args.get('p_id')
        product = Product.query.filter_by(prod_id=pid).delete()
        db.session.commit()
        flash(f'Your product  has been deleted!', 'success')
        return redirect(url_for('product'))
        return render_template('product.html', title='Products')
    else:
        pid = request.args.get('p_id')
        loc = Location.query.filter_by(loc_id=pid).delete()
        db.session.commit()
        flash(f'Your location  has been deleted!', 'success')
        return redirect(url_for('loc'))
        return render_template('loc.html', title='Locations')
