from flask import abort, flash, redirect, render_template

from . import app
from .constants import NOT_UNIQUE_CUSTOM_ID_MESSAGE_EXCITED
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """
    Viws функция для отображения главной страницы
    """
    form = URLMapForm()
    if form.validate_on_submit():
        if not form.custom_id.data:
            short = URLMap.get_unique_short_id()
        else:
            short = form.custom_id.data
            if URLMap.get(short=short) is not None:
                flash(NOT_UNIQUE_CUSTOM_ID_MESSAGE_EXCITED.format(custom_id=short))
                return render_template('yacut.html', form=form)
        data = {
            'url': form.original_link.data,
            'custom_id': short
        }
        urlmap = URLMap.from_dict(data)
        urlmap.save()
        return render_template('yacut.html', form=form, short=short)
    return render_template('yacut.html', form=form)


@app.route('/<short>')
def redirect_view(short):
    """
    View функция для редиректа по адресу оригинальной ссылки
    """
    urlmap = URLMap.get(short=short)
    if urlmap is None:
        abort(404)
    return redirect(urlmap.original)
