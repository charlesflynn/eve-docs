eve-docs
========

Work in progress. A Flask blueprint that generates documentation for [Eve](https://github.com/nicolaiarocci/eve) APIs. When complete, will generate html documentation and WADL specs in JSON and XML. Uses the [Flask-Bootstrap](https://github.com/mbr/flask-bootstrap) blueprint for html templates.

The `example.py` and `settings.py` files are from Nicola Iarocci's [eve-demo](https://github.com/nicolaiarocci/eve-demo) repo. `settings.py` is untouched. `example.py` has been modified to import and activate the blueprints:

  from flask.ext.bootstrap import Bootstrap
  from eve_docs import eve_docs

  ...

  Bootstrap(app)
  app.register_blueprint(eve_docs, url_prefix='/docs')
