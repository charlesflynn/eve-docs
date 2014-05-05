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
    for domain, resource in capp.config['DOMAIN'].items():
        if resource['item_methods'] or resource['resource_methods']:
            # hide the shadow collection for document versioning
            if 'VERSIONS' not in capp.config or not \
                    domain.endswith(capp.config['VERSIONS']):
                cfg['domains'][domain] = paths(domain, resource)
    return cfg


def identifier(resource):
    name = resource['item_lookup_field']
    ret = {
        'name': name,
        'type': 'string',
        'required': True,
    }
    return ret


def schema(resource, field=None):
    ret = []
    if field is not None:
        params = {field: resource['schema'][field]}
    else:
        params = resource['schema']
    for field, attrs in params.items():
        template = {
            'name': field,
            'type': 'None',
            'required': False,
        }
        template.update(attrs)
        ret.append(template)
        # If the field defines a schema, add any fields from the nested
        # schema prefixed by the field name
        if 'schema' in attrs and all(isinstance(v, dict)
                                     for v in attrs['schema'].values()):
            for subfield in schema(attrs):
                subfield['name'] = field + '.' + subfield['name']
                ret.append(subfield)
        # If the field defines a key schema, add any fields from the nested
        # schema prefixed by the field name and a * to denote the wildcard
        if 'keyschema' in attrs:
            attrs['schema'] = attrs.pop('keyschema')
            for subfield in schema(attrs):
                subfield['name'] = field + '.*.' + subfield['name']
                ret.append(subfield)
    return ret


def paths(domain, resource):
    ret = {}
    path = '/{}'.format(domain)
    pathtype = 'resource'
    ret[path] = methods(domain, resource, pathtype)

    primary = identifier(resource)
    path = '/{}/{}'.format(domain, pathparam(primary['name']))
    pathtype = 'item'
    ret[path] = methods(domain, resource, pathtype)

    alt = resource.get('additional_lookup', None)
    if alt is not None:
        path = '/{}/{}'.format(domain, pathparam(alt['field']))
        pathtype = 'additional_lookup'
        ret[path] = methods(domain, resource, pathtype, alt['field'])
    return ret


def methods(domain, resource, pathtype, param=None):
    ret = {}
    if pathtype == 'additional_lookup':
        method = 'GET'
        ret[method] = {}
        ret[method]['label'] = get_label(domain, pathtype, method)
        ret[method]['params'] = schema(resource, param)
    else:
        key = '{}_methods'.format(pathtype)
        methods = resource[key]
        for method in methods:
            ret[method] = {}
            ret[method]['label'] = get_label(domain, pathtype, method)
            ret[method]['params'] = []
            if method == 'POST':
                ret[method]['params'].extend(schema(resource))
            elif method == 'PATCH':
                ret[method]['params'].append(identifier(resource))
                ret[method]['params'].extend(schema(resource))
            elif pathtype == 'item':
                ret[method]['params'].append(identifier(resource))
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
