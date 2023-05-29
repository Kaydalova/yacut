from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (CUSTOM_ID, DATA_REQUIRED_MESSAGE,
                        LATIN_AND_NUMS_ONLY_MESSAGE, ORIGINAL_LINK,
                        REGEX_FOR_SHORL_URL, SUBMIT_MESSAGE)


class URLMapForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK,
        validators=[DataRequired(message=DATA_REQUIRED_MESSAGE)])
    custom_id = StringField(
        CUSTOM_ID,
        validators=[Length(min=2, max=16),
                    Optional(),
                    Regexp(
                        regex=REGEX_FOR_SHORL_URL,
                        message=LATIN_AND_NUMS_ONLY_MESSAGE)])
    submit = SubmitField(SUBMIT_MESSAGE)
