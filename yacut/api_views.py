import re
from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidApiUsage
from .models import LIMIT, URL_map
from .utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def add_link():
    data = request.get_json()
    if data is None:
        raise InvalidApiUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidApiUsage('"url" является обязательным полем!')
    short_id = data.get('custom_id')
    if short_id:
        if len(short_id) >= LIMIT or not re.match(r'^[a-zA-Z0-9]+$', short_id):
            raise InvalidApiUsage(
                'Указано недопустимое имя для короткой ссылки')
        if URL_map.query.filter_by(short=short_id).first():
            raise InvalidApiUsage(f'Имя "{short_id}" уже занято.')
    if short_id is None or short_id == "":
        short_id = get_unique_short_id()
    url = URL_map(
        original=data.get('url'),
        short=short_id
    )
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url = URL_map.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidApiUsage(
            'Указанный id не найден', HTTPStatus.NOT_FOUND
        )
    return jsonify(url.to_short_dict()), HTTPStatus.OK
