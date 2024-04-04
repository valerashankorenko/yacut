from http import HTTPStatus

from flask import flash, redirect, render_template

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        short_id = form.custom_id.data
        if URLMap.query.filter_by(short=short_id).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        if short_id == '' or short_id is None:
            short_id = get_unique_short_id()
            form.custom_id.data = short_id

        url = URLMap(
            original=form.original_link.data,
            short=short_id,
        )
        db.session.add(url)
        db.session.commit()
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@app.route('/<string:short_id>', methods=['GET'])
def redirect_to_original(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    if url_map:
        return redirect(url_map.original, HTTPStatus.FOUND)
