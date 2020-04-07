from flask import render_template, url_for, redirect, flash, request
from flaskinventory import app, db, login_manager, login_required, bcrypt, current_user, login_user, logout_user
from flaskinventory.forms import addproduct, addlocation, moveproduct, editproduct, editlocation, sellproduct, \
    addperson, editperson, editsellproduct, editmoveproduct, LoginForm, RegistrationForm, addkit, editkit, sellkit, \
    addMargin
from flaskinventory.models import Location, Product, Movement, Balance, Person, Sell, Stock, User, Kit, Margin
import time, datetime
from sqlalchemy.exc import IntegrityError


@app.template_filter('formatdatetime')
def format_datetime(value, format="%d %b %Y %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id)


@app.route("/")
@app.route("/stock")
def anon():
    return redirect(url_for('login'))


@app.route("/Overview")
@login_required
def overview():
    main_exist = Person.query.filter_by(name="CL_001").first()
    if not main_exist:
        main = Person(name="CL_001", phone="00000000", lastname="CL_OO1", code="CL_001")
        db.session.add(main)
        db.session.commit()

    admin_exist = User.query.filter_by(admin=True).first()
    if not admin_exist:
        password = bcrypt.generate_password_hash("ADMIN_12345@").decode('utf-8')
        admin = User(email="admin@inventory.com", authenticated=False, username="ADMIN", password=password, admin=True)
        db.session.add(admin)
        db.session.commit()

    cave_exist = Location.query.filter_by(loc_name="Cave").first()
    if not cave_exist:
        cave = Location(loc_name="Cave")
        db.session.add(cave)
        db.session.commit()

    main_exist = Location.query.filter_by(loc_name="Principal").first()
    if not main_exist:
        main = Location(loc_name="Principal")
        db.session.add(main)
        db.session.commit()

    bar_exist = Location.query.filter_by(loc_name="Bar").first()
    if not bar_exist:
        bar = Location(loc_name="Bar")
        db.session.add(bar)
        db.session.commit()

    sells = Sell.query.all()
    stocks = Stock.query.all()
    exists = bool(Sell.query.all())
    print(sells)
    if not exists:
        flash(f'Add products,locations and make transfers to view', 'info')
    return render_template('overview.html', sells=sells, stocks=stocks)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('overview'))
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
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, admin=True,
                    authenticated=True)
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
        prod = Product.query.filter_by(id=p_id).first()
        prod.prod_name = eform.editname.data
        prod.price = eform.price.data
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
        product = Product(prod_name=form.prodname.data, price=form.price.data,loc_id=1)
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
        print("location id", p_id)
        details = Location.query.all()
        loc = Location.query.filter_by(id=p_id).first()
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
    kitform = sellkit()
    sells = Sell.query.all()
    v_cave = 0
    v_bar = 0
    # for n in sells:
    #     if n.stocks.location.loc_name == "Cave":
    #         v_cave = v_cave + (n.qty * n.stocks.price)
    #     else:
    #         v_bar = v_bar + (n.qty * n.stocks.price)
    # print("Vente Bar", v_bar)
    # print("Vente Cave", v_cave)
    prod_choices = []
    kits_choices = []
    location_choices = []
    person_choices = Person.query.with_entities(Person.id, Person.name).all()
    products = Product.query.all()
    locations = db.session.query(Location).filter(Location.loc_name != "Principal")
    kits = Kit.query.all()

    for n in products:
        t = (n.id, n.prod_name + " ----->> " + n.location.loc_name + " (" + str(n.price) + " F CFA)")
        prod_choices.append(t)

    for n in locations:
        t = (n.id, n.loc_name)
        location_choices.append(t)

    for n in kits:
        t = (n.id, str(n.qty) + " A " + str(n.price) + " F CFA")
        kits_choices.append(t)

    prod_list_names = []
    kit_list_names = []
    person_list_names = []
    loc_list_names = []

    # passing list_names to the form for select field
    person_list_names += person_choices
    prod_list_names += prod_choices
    kit_list_names += kits_choices
    loc_list_names += location_choices
    # passing list_names to the form for select field
    form.product.choices = prod_list_names
    form.location.choices = loc_list_names
    form.person.choices = person_list_names

    kitform.person.choices = person_list_names
    kitform.product.choices = prod_list_names
    kitform.location.choices = loc_list_names
    kitform.kit.choices = kit_list_names

    exists = bool(Sell.query.all())
    if exists == False and request.method == 'GET':
        flash(f'Sell of products  to view', 'info')
    if request.method=='POST':
        if 'prodqty' in request.form:
            print("Form Person 0=>", form.person.data)
            timestamp = datetime.datetime.now()
            prod_stocks = Stock.query.filter_by(product_id=form.product.data).all()
            prod_sells = Sell.query.filter_by(product_id=kitform.product.data).all()
            product = Product.query.filter_by(id=form.product.data).first()
            av_qte = 0
            stock_prod_av_qte = 0
            sell_prod_av_qte = 0
            for n in prod_stocks:
                stock_prod_av_qte = stock_prod_av_qte + n.prod_qty

            for n in prod_sells:
                sell_prod_av_qte = sell_prod_av_qte + n.qty

            av_qte = stock_prod_av_qte - sell_prod_av_qte

            print("Qte Available", av_qte)
            print("Qte Incoming", form.prodqty.data)
            if form.prodqty.data <= av_qte:
                sell = Sell(date=timestamp, person_id=form.person.data,price=(product.price*form.prodqty.data),
                            qty=form.prodqty.data, credit=form.credit.data, location_id=form.location.data,product_id=form.product.data)
                db.session.add(sell)
                db.session.commit()
                flash(f'Your Sell has been added!', 'success')
            else:
                flash(f'Erreur! la quantité est trop élèvée par rapport au stock,Ravitaillez le stock SVP!!', 'danger')
            return redirect(url_for('sell'))
        elif 'kitqty' in request.form:
            print("Form Person 1 =>", kitform.person.data)
            timestamp = datetime.datetime.now()
            prod_stocks = Stock.query.filter_by(product_id=kitform.product.data).all()
            prod_sells = Sell.query.filter_by(product_id=kitform.product.data).all()
            product = Product.query.filter_by(id=kitform.product.data).first()
            kit = Kit.query.filter_by(id=kitform.kit.data).first()
            av_qte = 0
            stock_prod_av_qte=0
            sell_prod_av_qte=0
            for n in prod_stocks:
                stock_prod_av_qte = stock_prod_av_qte + n.prod_qty

            for n in prod_sells:
                sell_prod_av_qte = sell_prod_av_qte + n.qty

            av_qte=stock_prod_av_qte-sell_prod_av_qte
            print("Qte Available", av_qte)
            print("Qte Incoming", kitform.kitqty.data)
            if kitform.kitqty.data <= av_qte:
                sell = Sell(date=timestamp, person_id=kitform.person.data, price=(kit.price * kitform.kitqty.data),
                            qty=kitform.kitqty.data*kit.qty, credit=kitform.credit.data, location_id=kitform.location.data,product_id=kitform.product.data)
                db.session.add(sell)
                db.session.commit()
                flash(f'Your Sell has been added!', 'success')
            else:
                flash(f'Erreur! la quantité est trop élèvée par rapport au stock', 'danger')
            return redirect(url_for('sell'))
    return render_template('sell.html', title='Sells', form=form, sells=sells, eform=eform, kitform=kitform,
                           v_bar=v_bar, v_cave=v_cave)


# @app.route("/SellKit", methods=['GET', 'POST'])
# @login_required
# def sellkit():
#     form = sellproduct()
#     eform = editsellproduct()
#     kitform = sellkit()
#     sells = Sell.query.all()
#     v_cave = 0
#     v_bar = 0
#     for n in sells:
#         if n.stocks.location.loc_name == "Cave":
#             v_cave = v_cave + (n.qty * n.stocks.price)
#         else:
#             v_bar = v_bar + (n.qty * n.stocks.price)
#     print("Vente Bar", v_bar)
#     print("Vente Cave", v_cave)
#     exists = bool(Sell.query.all())
#     if exists == False and request.method == 'GET':
#         flash(f'Sell of products  to view', 'info')
#     # ----------------------------------------------------------
#
#     person_choices = Person.query.with_entities(Person.id, Person.name).all()
#     kits = Kit.query.all()
#     stocks = Stock.query.all()
#     prod_choices = []
#     kits_choices = []
#     for n in stocks:
#         t = (n.id, n.product.prod_name + " ----->> " + n.location.loc_name + " (" + str(n.product.price) + " F CFA)")
#         prod_choices.append(t)
#     for n in kits:
#         t = (n.id, str(n.qty) + " A " + str(n.price) + " F CFA")
#         kits_choices.append(t)
#     prod_list_names = []
#     kit_list_names = []
#     person_list_names = []
#     prod_list_names += prod_choices
#     person_list_names += person_choices
#     kit_list_names += kits_choices
#     # passing list_names to the form for select field
#     form.product.choices = prod_list_names
#     form.person.choices = person_list_names
#     kitform.person.choices = person_list_names
#     kitform.product.choices = prod_list_names
#     kitform.kit.choices = kit_list_names
#     # --------------------------------------------------------------
#     # send to db
#     if form.is_submitted() and request.method == 'POST':
#         print("Form Person=>", form.person.data)
#         timestamp = datetime.datetime.now()
#         prod_stocks = Stock.query.filter_by(id=form.product.data).all()
#         prod_av_qte = 0
#         for n in prod_stocks:
#             prod_av_qte = prod_av_qte + n.prod_qty
#
#         print("Qte Available", prod_av_qte)
#         print("Qte Incoming", form.prodqty.data)
#         if form.prodqty.data <= prod_av_qte:
#             sell = Sell(date=timestamp, person_id=form.person.data,
#                         qty=form.prodqty.data, credit=form.credit.data, stock_id=form.product.data)
#             db.session.add(sell)
#             db.session.commit()
#             flash(f'Your Sell has been added!', 'success')
#         else:
#             flash(f'Erreur! la quantité est trop élèvée par rapport au stock', 'danger')
#         return redirect(url_for('sell'))
#     elif kitform.is_submitted() and request.method == 'POST':
#         print("Kit Form", "Submited")
#     return render_template('sell.html', title='Sells', form=form, sells=sells, eform=eform, v_bar=v_bar, v_cave=v_cave,
#                            kitform=kitform)


@app.route("/Kit", methods=['GET', 'POST'])
@login_required
def kit():
    addkitform = addkit()
    editkitform = editkit()
    kits = Kit.query.all()
    exists = bool(kits)
    print("Edit submitted", editkitform.is_submitted())
    print("Add submitted", addkitform.is_submitted())
    if exists == False and request.method == 'GET':
        flash(f'Kit of products  to view', 'info')
    # elif editkitform.validate_on_submit() and request.method == 'POST':
    #     id = request.form.get("id", "")
    #     print("Request =>", request.form)
    #     print("Kit Id=>", id)
    #     kit = Kit.query.filter_by(id=id).first()
    #     print("Kit Price=>", kit.price)
    #     print("Kit Qty=>", kit.qty)
    #     kit.price = editkitform.price.data
    #     kit.qty = editkitform.qty.data
    #     db.session.commit()
    #     try:
    #         db.session.commit()
    #         flash(f'Your Kit  has been updated!', 'success')
    #         return redirect('/Kit')
    #     except IntegrityError:
    #         db.session.rollback()
    #         flash(f'This Kit already exists', 'danger')
    #         return redirect('/Kit')
    #     return render_template('kit.html', title='Kits', form=addkitform, kits=kits, eform=editkitform)
    elif addkitform.validate_on_submit():
        kit = Kit(price=addkitform.price.data, qty=addkitform.qty.data)
        db.session.add(kit)
        try:
            db.session.commit()
            flash(f'Your Kit  has been created!', 'success')
            return redirect('/Kit')
        except IntegrityError:
            db.session.rollback()
            flash(f'This Kit already exists', 'danger')
            return redirect('/Kit')
        return render_template('kit.html', title='Kits', form=addkitform, kits=kits, eform=editkitform)
    return render_template('kit.html', title='Kits', form=addkitform, kits=kits, eform=editkitform)


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
    loc_main = filter(lambda x: x.loc_name == 'Principal', loc_choices)
    prod_list_names = []
    dest_list_names = []
    prod_list_names += prod_choices
    dest_list_names += loc_main
    # passing list_names to the form for select field
    form.mprodname.choices = prod_list_names
    form.destination.choices = dest_list_names
    # --------------------------------------------------------------
    # send to db
    if form.is_submitted() and request.method == 'POST':
        timestamp = datetime.datetime.now()
        stock = Stock(created_at=timestamp, loc_id=form.destination.data,
                      product_id=form.mprodname.data, prod_qty=form.mprodqty.data)
        db.session.add(stock)
        db.session.commit()
        flash(f'Your Stock has been added!', 'success')
        return redirect(url_for('reception'))
    total = 0
    prix = 0
    for t in stocks:
        total = total + t.prod_qty
        prix = (t.product.price * t.prod_qty) + prix
    return render_template('reception.html', title='Receptions', form=form, eform=eform, stocks=stocks,
                           total=total, prix=prix)


@app.route("/Margin", methods=['GET', 'POST'])
@login_required
def margin():
    form = addMargin()
    eform = addMargin()
    margins = Margin.query.all()
    exists = bool(Margin.query.all())
    if exists == False and request.method == 'GET':
        flash(f'Margins products  to view', 'info')
    # ----------------------------------------------------------
    products = Product.query.all()
    prod_choices = []
    for n in products:
        t = (n.id, n.prod_name + " ----->> (" + str(n.price) + " F CFA)")
        prod_choices.append(t)
    loc_choices = Location.query.with_entities(Location.id, Location.loc_name).all()
    loc_main = filter(lambda x: x.loc_name != 'Principal', loc_choices)
    prod_list_names = []
    dest_list_names = []
    prod_list_names += prod_choices
    dest_list_names += loc_main
    # passing list_names to the form for select field
    form.mprodname.choices = prod_list_names
    eform.mprodname.choices = prod_list_names
    form.location.choices = dest_list_names
    eform.location.choices = dest_list_names
    # --------------------------------------------------------------
    # send to db
    if form.is_submitted() and request.method == 'POST':
        timestamp = datetime.datetime.now()
        margin = Margin(loc_id=form.location.data,
                        product_id=form.mprodname.data, value=form.value.data)
        db.session.add(margin)
        try:
            db.session.commit()
            flash(f'Your Margin has been added!', 'success')
        except IntegrityError:
            flash(f'La marge existe deja pour ce produit!', 'warning')
        return redirect(url_for('margin'))
    total = 0
    prix = 0
    return render_template('margin.html', title='Margin', form=form, eform=eform, margins=margins,
                           total=total, prix=prix)


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
        Product.query.filter_by(prod_id=pid).delete()
        db.session.commit()
        flash(f'Your product  has been deleted!', 'success')
        return redirect(url_for('product'))
        return render_template('product.html', title='Products')
    elif type == 'margin':
        pid = request.args.get('p_id')
        Margin.query.filter_by(id=pid).delete()
        db.session.commit()
        flash(f'Your Margin  has been deleted!', 'success')
        return redirect(url_for('margin'))
        return render_template('margin.html', title='Products')
    elif type == 'kit':
        pid = request.args.get('id')
        Kit.query.filter_by(id=pid).delete()
        db.session.commit()
        flash(f'Your Kit  has been deleted!', 'success')
        return redirect(url_for('kit'))
        return render_template('kit.html', title='Products')
    else:
        pid = request.args.get('p_id')
        loc = Location.query.filter_by(loc_id=pid).delete()
        db.session.commit()
        flash(f'Your location  has been deleted!', 'success')
        return redirect(url_for('loc'))
        return render_template('loc.html', title='Locations')
