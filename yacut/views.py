import random
import string

from flask import abort, flash, redirect, render_template

from . import app, db
from .constants import NUMBERS, SHORT_LENGTH, NOT_UNIQUE_CUSTOM_ID_MESSAGE
from .forms import URLMapForm
from .models import URLMap


def check_unique_url(short):
    """
    Функция проверяет существует ли в базе запись
    с указанной короткой ссылкой.
    """
    if URLMap.query.filter_by(short=short).first() is None:
        return True
    return False


def get_unique_short_id():
    """
    Функция генирирует уникальную короткую ссылку.
    Ссылка может состоять только из латинских букв
    и цифр от 0 до 9.
    """
    population = string.ascii_letters + NUMBERS
    while True:
        short = "".join(random.sample(population, SHORT_LENGTH))
        if check_unique_url(short):
            return short


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """
    Viws функция для отображения главной страницы
    """
    form = URLMapForm()
    if form.validate_on_submit():
        if not form.custom_id.data:
            short = get_unique_short_id()
        else:
            short = form.custom_id.data
            if not check_unique_url(short):
                flash(f'Имя {short} уже занято!')
                return render_template('yacut.html', form=form)
        urlmap = URLMap(
            original=form.original_link.data,
            short=short)
        db.session.add(urlmap)
        db.session.commit()
        return render_template('yacut.html', form=form, short=short)
    return render_template('yacut.html', form=form)


@app.route('/<short>')
def redirect_view(short):
    """
    View функция для редиректа по адресу оригинальной ссылки
    """
    urlmap = URLMap.query.filter_by(short=short).first()
    if urlmap is None:
        abort(404)
    return redirect(urlmap.original)
