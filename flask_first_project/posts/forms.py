from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, FileField, SelectField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        (5, 'Искусство'),
        (4, 'Музыка'),
        (3, 'Финансы'),
        (2, 'Путешествия'),
        (1, 'Развлечения'),
    ])
    picture = FileField(
        'Приложить фото к посту',
        validators=[FileAllowed(['pdf', 'png', 'jpg', 'jpeg', 'gif'])]
    )
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    body = StringField('Comment Text', validators=[DataRequired()])
    submit = SubmitField('Comment')
