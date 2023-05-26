from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (REGEX_FOR_SHORL_URL,
                        LATIN_AND_NUMS_ONLY_MESSAGE,
                        DATA_REQUIRED_MESSAGE,
                        SUBMIT_MESSAGE,
                        ORIGINAL_LINK, CUSTOM_ID)


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
