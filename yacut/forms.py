from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp


class URLMapForm(FlaskForm):
    """Класс формы проекта."""

    original_link = URLField(
        'Ваша длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'), URL(
            require_tld=True, message='Некорректный URL')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, 16), Optional(), Regexp(
            r'^[A-Za-z0-9]+$',
            message='Можно использовать только [A-Za-z0-9]')]
    )
    submit = SubmitField('Создать')