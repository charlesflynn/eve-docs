Eve-docs
========

A blueprint that generates documentation for
`Eve <https://github.com/nicolaiarocci/eve>`__ APIs in HTML and JSON
formats. Eve-docs creates the documentation from your existing Eve
configuration file, with no additional configuration required.

Installation
~~~~~~~~~~~~

Clone this repo into your Eve application and modify your launch script
to activate the blueprints:

::

    from flask.ext.bootstrap import Bootstrap
    from eve_docs import eve_docs
    ...
    Bootstrap(app)
    app.register_blueprint(eve_docs, url_prefix='/docs')

After restarting, documentation is availabile at the ``url_prefix``
defined in your launch script. ``example.py`` shows how to do this using
the launch script from Nicola Iarocci's
`eve-demo <https://github.com/nicolaiarocci/eve-demo>`__ repo.


Additional Documentation
~~~~~~~~~~~~~~~~~~~~~~~~

You may want to add descriptions for resources to eve-docs.
This is possible by adding an additional key 'description' to the resource 
definition at the same level as the 'schema'.  
Inside the description, you can add 3 different types of additional 
documentation: 

- 'general': A general description of the resource.

- 'methods': For each of the methods eve-docs lists, you can add a method-related description.

- 'fields': You can add a description to each field of the schema.

An example of this additional description can be found in example.py for 
the 'people' resource:

::  

    'description': {
            'general': 'Represents people who work at the company.',
            'methods': {
                'DELETE': 'DELETE may need special authorization.'
            },
            'fields': {
                'role': 'The role defines the place of this person within the '
                        'company',
                'location': 'A dict for the address of this person.',
                'born': 'Is datetime object, but only the date information is '
                        'relevant.'
            }
        }


HTML output
~~~~~~~~~~~

The HTML documentation is produced using the
`Flask-Bootstrap <https://github.com/mbr/flask-bootstrap>`__ blueprint.
Expand each domain to show available endpoint methods, and further
expand each method to show parameter details. A screenshot with one
method expanded follows, and you can also view a `fully expanded example 
|Sample output| image:: screenshot.png  

JSON output
~~~~~~~~~~~

Documentation is also exposed as JSON at ``url_prefix/spec.json`` for
programmatic consumption. Example output:

::

    {
      "base": "http://localhost:5000",
      "domains": {
        "people": {
          "/people/{_id}": {
            "GET": {
              "label": "Retrieve a person",
              "params": [
                {
                  "name": "_id",
                  "type": "string",
                  "required": true
                }
              ]
              ...

License
~~~~~~~

Released under the `MIT
License <http://www.opensource.org/licenses/MIT>`__.

.. |Sample output| image:: http://charonex.com/img/evedocs-example.png
