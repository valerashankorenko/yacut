from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id
from .validators import validate_url


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    url = URLMap()
    if data is None:
        raise InvalidAPIUsage(
            'Отсутствует тело запроса'
        )
    if 'url' not in data:
        raise InvalidAPIUsage(
            '\"url\" является обязательным полем!'
        )
    if 'custom_id' not in data or not data.get('custom_id'):
        custom_id = get_unique_short_id()
        data['custom_id'] = str(custom_id)
        url.from_dict(data)
        db.session.add(url)
        db.session.commit()
        return jsonify(url.to_dict()), HTTPStatus.CREATED

    url.from_dict(data)
    if URLMap.query.filter_by(short=url.short).first():
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    short_id = data.get('custom_id') or get_unique_short_id()
    if short_id is None:
        short_id = get_unique_short_id()
    elif not validate_url(short_id) or len(short_id) > 16:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK
