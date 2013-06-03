from flask import Blueprint, render_template, current_app, jsonify
from config import get_cfg
from wadl import get_wadl
import pprint


eve_docs = Blueprint('eve_docs', __name__,
                     template_folder='templates')


@eve_docs.route('/')
def index():
    cfg = get_cfg()
    return render_template('index.html', cfg=cfg)


@eve_docs.route('/wadl.json')
def wadl():
    wadl = get_wadl()
    return jsonify(wadl)


@eve_docs.route('/rawcfg')
def rawcfg():
    cfg = get_cfg()
    pp = pprint.PrettyPrinter(indent=1)
    cfg = pp.pformat(cfg)
    return render_template('rawcfg.html', cfg=cfg)
