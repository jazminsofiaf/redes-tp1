from flask import abort, make_response

# Data to serve with our API
example = {
    'domain': 'jaz.domain',
    'ip':  '157.99.45.33',
    'custom': True
}


def get_ip(domain):
    """
    Esta funcion maneja el request GET /api/domains/{domain}
    return: 200 IP asociado a un dominio en particular
    """

    return make_response(example, 200)
