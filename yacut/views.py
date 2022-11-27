from flask import flash, redirect, render_template

from . import app, db
from .forms import YacutForm
from .models import URL_map
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = YacutForm()
    if form.validate_on_submit():
        short_id = form.custom_id.data
        if URL_map.query.filter_by(short=short_id).first():
            flash(f'Имя {short_id} уже занято!')
            return render_template('index.html', form=form)
        if short_id is None or short_id == '':
            short_id = get_unique_short_id()
        yacut = URL_map(
            original=form.original_link.data,
            short=short_id
        )
        db.session.add(yacut)
        db.session.commit()
        return render_template('index.html', form=form, short=short_id), 200
    return render_template('index.html', form=form)


@app.route('/<string:custom_id>')
def redirect_view(custom_id):
    url_map = URL_map.query.filter_by(short=custom_id).first_or_404()
    return redirect(url_map.original)
