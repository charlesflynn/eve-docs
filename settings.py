# -*- coding: utf-8 -*-

"""
    eve-demo settings
    ~~~~~~~~~~~~~~~~~

    Settings file for our little demo.

    PLEASE NOTE: We don't need to create the two collections in MongoDB.
    Actually, we don't even need to create the database: GET requests on an
    empty/non-existant DB will be served correctly ('200' OK with an empty
    collection); DELETE/PATCH will receive appropriate responses ('404' Not
    Found), and POST requests will create database and collections when needed.
    Keep in mind however that such an auto-managed database will most likely
    perform poorly since it lacks any sort of optimized index.

    :copyright: (c) 2012 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""

import os

# We want to seamlessy run our API both locally and on Heroku so:
if os.environ.get('PORT'):
    # We're hosted on Heroku!  Use the MongoHQ sandbox as our backend.
    MONGO_HOST = 'alex.mongohq.com'
    MONGO_PORT = 10047
    MONGO_USERNAME = 'evedemo'
    MONGO_PASSWORD = 'evedemo'
    MONGO_DBNAME = 'app9346575'

    # also, correctly set the API entry point
    SERVER_NAME = 'eve-demo.herokuapp.com'
else:
    # Running on local machine. Let's just use the local mongod instance.
    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    MONGO_USERNAME = 'user'
    MONGO_PASSWORD = 'user'
    MONGO_DBNAME = 'apitest'

    # let's not forget the API entry point
    SERVER_NAME = 'localhost:5000'


# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

# We enable standard client cache directives for all resources exposed by the
# API. We can always override these global settings later.
CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20

# Our API will expose two resources (MongoDB collections): 'people' and
# 'works'. In order to allow for proper data validation, we define beaviour
# and structure.
people = {
    # 'title' tag used in item links.
    'item_title': 'person',

    # by default the standard item entry point is defined as
    # '/people/<ObjectId>/'. We leave it untouched, and we also enable an
    # additional read-only entry point. This way consumers can also perform GET
    # requests at '/people/<lastname>/'.
    'additional_lookup': {
        'url': '[\w]+',
        'field': 'lastname'
    },

    # Schema definition, based on Cerberus grammar. Check the Cerberus project
    # (https://github.com/nicolaiarocci/cerberus) for details.
    'schema': {
        'firstname': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 10,
        },
        'lastname': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 15,
            'required': True,
            # talk about hard constraints! For the purpose of the demo
            # 'lastname' is an API entry-point, so we need it to be unique.
            'unique': True,
        },
        # 'role' is a list, and can only contain values from 'allowed'.
        'role': {
            'type': 'list',
            'allowed': ["author", "contributor", "copy"],
        },
        # An embedded 'strongly-typed' dictionary.
        'location': {
            'type': 'dict',
            'schema': {
                'address': {'type': 'string'},
                'city': {'type': 'string'}
            },
        },
        'born': {
            'type': 'datetime',
        },
    },
    # The key we defined for special documentaton
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
}

works = {
    #'item_methods': ['GET'],
    # if 'item_title' is not provided Eve will just strip the final
    # 's' from resource name, and use it as the item_title.
    #'item_title': 'work',

    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    'schema': {
        'title': {
            'type': 'string',
            'required': True,
        },
        'description': {
            'type': 'string',
        },
        'owner': {
            'type': 'objectid',
            'required': True,
            # referential integrity constraint: value must exist in the
            # 'people' collection. Since we aren't declaring a 'field' key,
            # will default to `people._id` (or, more precisely, to whatever
            # ID_FIELD value is).
            'data_relation': {
                'collection': 'people'
            }
        },
    }
}

# The DOMAIN dict explains which resources will be available and how they will
# be accessible to the API consumer.
DOMAIN = {
    'people': people,
    'works': works,
}
