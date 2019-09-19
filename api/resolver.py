import dns.resolver

ip_regex = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"

"""
def resolveDNS(hostname):
    result = []
    for answer in dns.resolver.query(hostname, "A").response.answer:
        recodt_type = dns.rdatatype.to_text(answer.rdtype)
        if(recodt_type != "A"):
            continue
        result.extend(re.findall(ip_regex, answer.to_text()))
    return result
"""

def resolveDNS(hostname):
    return [str(a) for a in dns.resolver.query(hostname)]


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
