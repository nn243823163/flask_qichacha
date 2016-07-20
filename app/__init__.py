#coding:utf-8
from flask import *
from werkzeug.routing import BaseConverter
from .views import init_views





def creat_app():
    app =  Flask(__name__)
    app.config.from_pyfile('..\local_settings.py')
    init_views(app)
    return app


# if __name__ == '__main__':
#     manage.run()
    # app.run(debug=True)

# from flask import Flask
# from werkzeug.routing import BaseConverter
# class RegexConverter(BaseConverter):
#     def __init__(self, map, *args):
#         # super(RegexConverter,self).__init__(map)
#         self.map = map
#         self.regex = args[0]
#
# app = Flask(__name__)
# app.url_map.converters['regex'] = RegexConverter

# @app.route('/view/<regex("[a-zA-Z0-9]+"):uuid>/')
# def view(uuid):
#     """
#     url: /view/1010000000125259/
#     result: view uuid:1010000000125259
#     """
#     return "view uuid: %s" % (uuid)
#
# @app.route('/<regex(".*"):url>')
# def not_found(url):
#     """
#     url: /hello
#     result: not found: 'hello'
#     """
#     return "not foundnn: '%s'" % (url)


# if __name__ == '__main__':
#     app.run(debug=True)
