from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

ALLOWED = ('jpg', 'jpeg', 'png', 'gif')

class UploadForm(FlaskForm):
    file = FileField('File', validators=[
        FileRequired(),
        FileAllowed(ALLOWED, 'Images only')
    ])
    submit = SubmitField('Upload')
