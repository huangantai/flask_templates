from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length

class HelloForm(FlaskForm):
    name=StringField("Name",validators=[DataRequired(message="name must be not empty"),Length(1,20)])
    body=TextAreaField("Message",validators=[DataRequired(message="message must be not empty"),Length(1,200)])
    submit=SubmitField()

