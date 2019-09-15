from flask import abort, make_response
import dns.resolver

def resolveDNS(hostname):
    result = []
    for answer in dns.resolver.query(hostname, "A").response.answer:
        recodt_type = dns.rdatatype.to_text(answer.rdtype)
        if(recodt_type != "A"):
            continue
        result.extend(list(map(lambda x : x[len(x) - 15: len(x)], answer.to_text().split("\n"))))
    return result


def get_ips(hostname):
    result = []
    try:
        result.extend(resolveDNS(hostname))
    except dns.resolver.NXDOMAIN:
        print("No such domain %s", hostname)
    except dns.resolver.Timeout:
        print("Timed out while resolving %s",hostname)
    except dns.exception.DNSException as e:
        print(" DNSException %s while resolving %s",e, hostname)
    finally:
        return result

###############################################################################

# Data to serve with our API
domains = {
    'custom.domain':{
        'domain': 'custom.domain',
        'ip':  '99.99.99.99',
        'custom': True
    }
}

def all_custom_domains():
    """
    Esta funcion maneja el request GET /api/custom-domains?q={filter}

    :return: 200 lista de todos los domains
    """
    # Create the list of people from our data
    return list(domains.values())



def get_domain(domain):
    """
    Esta funcion maneja el request GET /api/domains/{domain}
    return: 200 IP asociado a un dominio en particular
    """
    ip_list = get_ips(domain)
    if not ip_list:
        return abort(404, 'domain not found')

    ip = ip_list[0].strip()
    response  = {
        'domain': domain,
        'ip':  ip,
        'custom': True
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
    print(domain)
    domains[domain_name] = domain
    print(domains)

    return make_response(domain, 201)

def delete_custom_domain(domain):
        """Esta funcion maneja el request DELETE /api/custom-domains/{domain}

        :return: 204 domain, 404 domain no encontrado
        """
        if domain not in domains:
            return abort(404, 'domain not found')

        del domains[domain]

        domain_deleted = {
             'domain': domain
        }
        return make_response(domain_deleted, 200)
