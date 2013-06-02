from flask import Blueprint, render_template, current_app, url_for, jsonify
import pprint


eve_docs = Blueprint('eve_docs', __name__,
                     template_folder='templates')


def get_labels():
    labels = {
        'item_methods': {
            'GET': 'Retrieve a single entry',
            'PATCH': 'Update a single entry',
            'DELETE': 'Delete a single entry',
        },
        'resource_methods': {
            'GET': 'Retrieve a list of entries',
            'POST': 'Create a new entry',
            'DELETE': 'Delete all entries',
        },
    }
    return labels


def get_cfg():
    fields = (
        'API_VERSION',
        'DOMAIN',
        'ID_FIELD',
        'PREFERRED_URL_SCHEME',
        'SERVER_NAME',
        'URL_PREFIX',
    )
    cfg = {}
    for field in fields:
        cfg[field] = current_app.config[field]
    cfg['LABELS'] = get_labels()
    return cfg


def get_wadl():
    cfg = get_cfg()
    wadl = {}
    id = '{{{0}}}'.format(cfg['ID_FIELD'])
    for name, content in cfg['DOMAIN'].items():
        endpoint = {}
        params = []
        for name, attrs in content['schema'].items():
            required = attrs.get('required', False)
            params.append({
                'name': name,
                'style': 'query',
                'type': attrs['type'],
                'required': required,
            })
        for item in content['item_methods']:
            url = '/{}/{}'.format(content['url'], id)
            endpoint[item] = [{
                'name': cfg['ID_FIELD'],
                'style': 'template',
                'required': True,
            }]
            if item in ('POST', 'PATCH'):
                endpoint[item].extend(params)
        wadl[url] = endpoint
        endpoint = {}
        if 'additional_lookup' in content:
            field = content['additional_lookup']['field']
            lookup = '{{{0}}}'.format(field)
            url = '/{}/{}'.format(content['url'], lookup)
            endpoint['GET'] = [{
                'name': field,
                'style': 'template',
                'type': content['schema'][field]['type'],
                'required': True,
            }]
            wadl[url] = endpoint
            endpoint = {}
        for item in content['resource_methods']:
            url = '/{}'.format(content['url'])
            if item in ('POST', 'PATCH'):
                endpoint[item] = params
        wadl[url] = endpoint
    return wadl


@eve_docs.route('/')
def index():
    cfg = get_cfg()
    return render_template('index.html', cfg=cfg)


@eve_docs.route('/application.<type>')
def wadlspec(type='json'):
    wadl = get_wadl()
    return jsonify(wadl)


@eve_docs.route('/rawcfg')
def rawcfg():
    cfg = get_cfg()
    pp = pprint.PrettyPrinter(indent=1)
    cfg = pp.pformat(cfg)
    return render_template('rawcfg.html', cfg=cfg)
