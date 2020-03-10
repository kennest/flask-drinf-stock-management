from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Email, Length, EqualTo


class addproduct(FlaskForm):
    prodname = StringField('Product Name', validators=[DataRequired()])
    price = IntegerField('Prix', validators=[DataRequired()])
    prodsubmit = SubmitField('Save Changes')


class addkit(FlaskForm):
    qty = IntegerField('Qte', validators=[DataRequired()])
    price = IntegerField('Prix', validators=[DataRequired()])
    kitsubmit = SubmitField('Save')


class editkit(FlaskForm):
    qty = IntegerField('Qte', validators=[DataRequired()])
    price = IntegerField('Prix', validators=[DataRequired()])
    kiteditsubmit = SubmitField('Save Changes')


class addMargin(FlaskForm):
    mprodname = SelectField(
        'Nom de la boisson')
    location = SelectField(
        'Emplacements')
    value = IntegerField('Valeur', validators=[DataRequired()])
    marginsubmit = SubmitField('Save Changes')


class editproduct(FlaskForm):
    editname = StringField('Product Name', validators=[DataRequired()])
    price = IntegerField('Prix', validators=[DataRequired()])
    editsubmit = SubmitField('Save Changes')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class addlocation(FlaskForm):
    locname = StringField('Location Name', validators=[DataRequired()])
    locsubmit = SubmitField('Save Changes')


class editlocation(FlaskForm):
    editlocname = StringField('Location Name', validators=[DataRequired()])
    editlocsubmit = SubmitField('Save Changes')


class moveproduct(FlaskForm):
    mprodname = SelectField(
        'Nom de la boisson')
    destination = SelectField(
        'Destination')
    mprodqty = IntegerField('Quantité', validators=[DataRequired()])
    movesubmit = SubmitField('Sauvergarder')


class editmoveproduct(FlaskForm):
    mprodname = SelectField(
        'Nom de la boisson')
    destination = SelectField(
        'Emplacement')
    mprodqty = IntegerField('Quantité', validators=[DataRequired()])
    editsubmit = SubmitField('Sauvegarder')


class sellproduct(FlaskForm):
    product = SelectField(
        'Nom du produit')
    person = SelectField(
        'Nom du client')
    prodqty = IntegerField('Quantité', validators=[DataRequired()])
    credit = BooleanField('à Crèdit')
    sellsubmit = SubmitField('Sauvegarder')


class sellkit(FlaskForm):
    product = SelectField(
        'Nom du produit')
    person = SelectField(
        'Nom du client')
    kit = SelectField(
        'Kit')
    kitqty = IntegerField('Nombre de kits', validators=[DataRequired()])
    credit = BooleanField('à Crèdit')
    sellkitsubmit = SubmitField('Sauvegarder')


class editsellproduct(FlaskForm):
    product = SelectField(
        'Product Name')
    person = SelectField(
        'Person Name')
    prodqty = IntegerField('Quantity', validators=[DataRequired()])
    credit = BooleanField('Credit')
    sellsubmit = SubmitField('Save')


class addperson(FlaskForm):
    personname = StringField('Name', validators=[DataRequired()])
    personlastname = StringField('LastName')
    personcode = StringField('Code')
    personphone = StringField('Phone')
    personsubmit = SubmitField('Save')


class editperson(FlaskForm):
    editpersonname = StringField('Name', validators=[DataRequired()])
    editpersonlastname = StringField('LastName')
    editpersoncode = StringField('Code', validators=[DataRequired()])
    editpersonphone = StringField('Phone')
    editpersonsubmit = SubmitField('Save')
