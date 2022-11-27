from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp


class YacutForm(FlaskForm):
    original_link = URLField(
        'Введите длинную ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    URL(message='Неккоректная ссылка')]
    )
    custom_id = URLField(
        'Введите вашу короткую ссылку',
        validators=[Length(1, 16), Optional(), Regexp(
                    r'^[a-zA-Z0-9]+$')]
    )
    submit = submit = SubmitField('Создать')
