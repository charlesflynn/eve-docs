from flask import Blueprint, render_template, jsonify
from .config import get_cfg


eve_docs = Blueprint('eve_docs', __name__,
                     template_folder='templates')


@eve_docs.route('/')
def index():
    cfg = get_cfg()
    return render_template('index.html', cfg=cfg)


@eve_docs.route('/spec.json')
def spec():
    spec = get_cfg()
    return jsonify(spec)
