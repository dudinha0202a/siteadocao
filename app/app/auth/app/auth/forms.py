from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired(), Length(max=120)])
    email = StringField("E-mail", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Criar conta")

class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")