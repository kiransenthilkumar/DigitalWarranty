from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField, DateField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    brand = StringField('Brand', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    purchase_date = DateField('Purchase Date', validators=[DataRequired()])
    warranty_duration = IntegerField('Warranty Duration (months)', validators=[DataRequired(), NumberRange(min=1)])
    price = FloatField('Price (₹)', validators=[DataRequired(), NumberRange(min=0)])
    receipt = StringField('Receipt Number')
    receipt_file = FileField('Receipt/Invoice')
    product_image = FileField('Product Image')
    submit = SubmitField('Add Product')

class SettingsForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[EqualTo('new_password')])
    submit = SubmitField('Update Settings')