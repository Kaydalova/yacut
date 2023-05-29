import string

SHORT_LENGTH = 6
POPULATION_FOR_RANDOM_SHORT = string.ascii_letters + "0123456789"
MAX_SHORT_LENGTH = 16
MAX_ORIGINAL_LENGTH = 512
REGEX_FOR_SHORL_URL = r'^[a-zA-Z\d]{1,16}$'
REGEX_FOR_ORIGINAL_URL = r'((http|https)?:\/\/[\S]+)'


#ERROR MESSAGES
EMPTY_BODY_MESSAGE = 'Отсутствует тело запроса'
NO_URL_MESSAGE = '"url" является обязательным полем!'
INVALID_CUSTOM_ID_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
INVALID_URL_MESSAGE = 'Неверный формат URL'
NOT_UNIQUE_CUSTOM_ID_MESSAGE = 'Имя "{custom_id}" уже занято.'
NOT_UNIQUE_CUSTOM_ID_MESSAGE_EXCITED = 'Имя {custom_id} уже занято!'
ID_NOT_FOUND_MESSAGE = 'Указанный id не найден'
LATIN_AND_NUMS_ONLY_MESSAGE = 'Можно только латинские буквы и цифры'
DATA_REQUIRED_MESSAGE = 'Обязательное поле'
OUT_OF_SHORTS_MESSAGE = 'Кончились варианты для коротких ссылок'

SUBMIT_MESSAGE = 'Создать'
ORIGINAL_LINK = 'Длинная ссылка'
CUSTOM_ID = 'Ваш вариант короткой ссылки'
