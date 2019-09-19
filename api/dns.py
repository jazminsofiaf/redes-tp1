from flask import abort, make_response
import api.resolver as resolver

# Data to serve with our API
domains = {
    'custom.domain':{
        'domain': 'custom.domain',
        'ip':  '99.99.99.99',
        'custom': True
    }
}

counter = {
    'custom.domain':{
        'ips': {
            '99.99.99.99': 1,
            '99.99.99.91': 0
        }
    }
}

def all_custom_domains(**kwargs):
    """
    Esta funcion maneja el request GET /api/custom-domains?q={filter}

    :return: 200 lista de todos los domains
    """
    # Create the list of people from our data
    result = list(domains.values())
    substring = kwargs.get('q')
    if(substring):
        result = list(filter(lambda d: substring in d['domain'],result))
    return result



def get_domain(domain):
    """
    Esta funcion maneja el request GET /api/domains/{domain}
    return: 200 IP asociado a un dominio en particular
    """
    if(domain in domains.keys()):
        return make_response(domains[domain], 200)

    ip_list = resolver.get_ips(domain)
    if not ip_list:
        return abort(404, 'domain not found')

    ips_count = { ip: 0 for ip in ip_list }
    if(domain in counter):
        used_ips = counter[domain]
        ips_count = { ip: used_ips[ip] if (ip in used_ips) else 0 for ip in ip_list }

    ip = (min(ips_count, key=ips_count.get)).strip()
    ips_count[ip] = max(ips_count.values()) + 1

    print(ips_count)
    counter[domain] = ips_count
    response  = {
        'domain': domain,
        'ip':  ip,
        'custom': False
    }
    return make_response(response, 200)



def new_custom_domain(**kwargs):
    """
    Esta funcion maneja el request POST /api/custom-domain
    :param: dominio a crear en la lista de custom domains
    :return: 201 dominio creado, 400 dominio duplicado
    """
    domain = kwargs.get('body')
    domain_name = domain.get('domain')
    ip = domain.get('ip')

    if not domain_name or not ip:
        return abort(400, 'Faltan datos para crear el custom domain')

    duplicated = False
    for existing_domain in domains.values():
        duplicated = (domain_name == existing_domain.get('domain') or ip == existing_domain.get('ip'))
        if duplicated: break

    if duplicated:
        return abort(400, 'custom domain already exists')

    domain['custom'] = True
    domains[domain_name] = domain

    return make_response(domain, 201)

def update_custom_domain(domain, **kwargs):
    """
    Esta funcion maneja el request PUT /api/custom-domains/{domain}
    :param: dominio a crear en la lista de custom domains
    :return: 201 dominio creado, 400 dominio duplicado
    """
    domain_obj = kwargs.get('body')
    domain_name = domain_obj.get('domain')
    ip = domain_obj.get('ip')

    if not domain_name or not ip or domain_name != domain:
        return abort(400, 'payload is invalid')

    if not domain_name in domains.keys():
        return abort(404, 'domain not found')


    domain_obj['custom'] = True
    domains[domain_name] = domain_obj

    return make_response(domain_obj, 200)

def delete_custom_domain(domain):
        """Esta funcion maneja el request DELETE /api/custom-domains/{domain}

        :return: 200 domain, 404 domain no encontrado
        """
        if domain not in domains:
            return abort(404, 'domain not found')

        del domains[domain]

        domain_deleted = {
             'domain': domain
        }
        return make_response(domain_deleted, 200)
