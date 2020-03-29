from urllib.parse import parse_qs, urlencode, urlparse

from django.template import Library

register = Library()

QUESTION_MARK = "?"


@register.simple_tag
def set_url_param(full_path, param, value):
    if QUESTION_MARK not in full_path:
        full_path += "{}{}={}".format(QUESTION_MARK, param, value)
        return full_path

    base = full_path.split(QUESTION_MARK)[0]
    parsed_url = urlparse(full_path)
    url_params = parse_qs(parsed_url.query)

    if param in url_params:
        url_params[param][0] = value
    else:
        url_params[param] = [value]

    return base + QUESTION_MARK + urlencode(url_params, doseq=True)
