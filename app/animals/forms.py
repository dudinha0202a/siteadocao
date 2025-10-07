from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class AnimalForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired(), Length(max=120)])
    species = StringField("Espécie", validators=[DataRequired(), Length(max=50)])
    breed = StringField("Raça", validators=[Optional(), Length(max=120)])
    age = StringField("Idade", validators=[Optional(), Length(max=50)])
    size = StringField("Porte", validators=[Optional(), Length(max=30)])
    sex = StringField("Sexo", validators=[Optional(), Length(max=10)])
    city = StringField("Cidade", validators=[Optional(), Length(max=120)])
    photo_url = StringField("URL da foto", validators=[Optional(), Length(max=300)])
    description = TextAreaField("Descrição", validators=[Optional()])
    available = BooleanField("Disponível", default=True)
    submit = SubmitField("Salvar")
