from flask_wtf import FlaskForm
from wtforms import IntegerField,SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired,FileAllowed


class MyForm(FlaskForm):
    number = IntegerField('number_pics', validators=[DataRequired()],\
                          render_kw={"placeholder": "Insert number of photos"})
    photo = FileField('image', validators=[FileRequired(),FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Submit")
