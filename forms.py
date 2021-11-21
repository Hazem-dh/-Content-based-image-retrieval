from flask_wtf import FlaskForm
from wtforms import IntegerField,SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired,FileAllowed


class MyForm(FlaskForm):
    number = IntegerField('number_pics', validators=[DataRequired()])
    photo = FileField('image', validators=[FileRequired(),FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Submit")
