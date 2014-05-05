from flask import current_app as capp
from eve.utils import home_link
from .labels import LABELS


def get_cfg():
    cfg = {}
    base = home_link()['href']
    if '://' not in base:
        protocol = capp.config['PREFERRED_URL_SCHEME']
        base = '{}://{}'.format(protocol, base)
    cfg['base'] = base
    cfg['domains'] = {}
    cfg['server_name'] = capp.config['SERVER_NAME']
    cfg['api_name'] = capp.config.get('API_NAME', 'API')
    for domain in capp.config['DOMAIN'].keys():
        if capp.config['DOMAIN'][domain]['item_methods'] or \
                capp.config['DOMAIN'][domain]['resource_methods']:
            # hide the shadow collection for document versioning
            if 'VERSIONS' not in capp.config or not \
                    domain.endswith(capp.config['VERSIONS']):
                cfg['domains'][domain] = {}
                cfg['domains'][domain] = paths(domain)
    return cfg


def identifier(domain):
    name = capp.config['DOMAIN'][domain]['item_lookup_field']
    ret = {
        'name': name,
        'type': 'string',
        'required': True,
    }
    return ret


def schema(domain, field=None):
    ret = []
    if field is not None:
        params = {field: capp.config['DOMAIN'][domain]['schema'][field]}
    else:
        params = capp.config['DOMAIN'][domain]['schema']
    for field, attrs in params.items():
        template = {
            'name': field,
            'type': 'None',
            'required': False,
        }
        template.update(attrs)
        ret.append(template)
    return ret


def paths(domain):
    ret = {}
    path = '/{}'.format(domain)
    pathtype = 'resource'
    ret[path] = methods(domain, pathtype)

    primary = identifier(domain)
    path = '/{}/{}'.format(domain, pathparam(primary['name']))
    pathtype = 'item'
    ret[path] = methods(domain, pathtype)

    alt = capp.config['DOMAIN'][domain].get('additional_lookup', None)
    if alt is not None:
        path = '/{}/{}'.format(domain, pathparam(alt['field']))
        pathtype = 'additional_lookup'
        ret[path] = methods(domain, pathtype, alt['field'])
    return ret


def methods(domain, pathtype, param=None):
    ret = {}
    if pathtype == 'additional_lookup':
        method = 'GET'
        ret[method] = {}
        ret[method]['label'] = get_label(domain, pathtype, method)
        ret[method]['params'] = schema(domain, param)
    else:
        key = '{}_methods'.format(pathtype)
        methods = capp.config['DOMAIN'][domain][key]
        for method in methods:
            ret[method] = {}
            ret[method]['label'] = get_label(domain, pathtype, method)
            ret[method]['params'] = []
            if method == 'POST':
                ret[method]['params'].extend(schema(domain))
            elif method == 'PATCH':
                ret[method]['params'].extend(schema(domain))
                ret[method]['params'].append(identifier(domain))
            elif pathtype == 'item':
                ret[method]['params'].append(identifier(domain))
    return ret


def pathparam(param):
    return '{{{}}}'.format(param)


def get_label(domain, pathtype, method):
    verb = LABELS[method]
    if method == 'POST' or pathtype != 'resource':
        noun = capp.config['DOMAIN'][domain]['item_title']
        article = 'a'
    else:
        noun = domain
        article = 'all'
    return '{} {} {}'.format(verb, article, noun)
