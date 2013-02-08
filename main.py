#!/usr/bin/env python

# Copyright (C) 2013 Galaxy Team

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# setup the connection to the database before anything else
import os
# from sqlalchemy import create_engine
# from sqlalchemy import Table, Column, Integer, String, MetaData
# engine = create_engine(os.environ.get(
#     'DATABASE_URL', 'postgresql://postgres:pass@localhost:5432/'))
# # conn = engine.connect()

# metadata = MetaData(engine)
# events_table = Table('events', metadata,
#     Column('event_id', Integer, primary_key=True),
#     Column('event_info', String),
# )
# # events.select()
# metadata.create_all(engine)


import sys
import tornado
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.template

sys.argv.append('--logging=INFO')
tornado.options.parse_command_line()


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
loader = tornado.template.Loader(template_dir)
render = lambda handler, name, values: loader.load(name).generate(static_url=handler.static_url, **values)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(render(self, 'home.html', {}))


class GithubButtonHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(render(self, 'github-btn.html', {}))


class GitHubStream(tornado.web.RequestHandler):
    def get(self):
        self.write(render(self, 'github_stream.html', {}))

# import events
# import json


# class StreamActual(tornado.web.RequestHandler):
#     def get(self):
#         self.write(json.dumps(list(
#             events.get_events())))

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": True,
}


application = tornado.web.Application([
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': settings['static_path']}),
    (r"/", MainHandler),
    (r"/github", GitHubStream),
    (r"/github-btn", GithubButtonHandler),
    # ('/stream', StreamActual)
], **settings)


def main():
    application.listen(os.environ.get('PORT', 8888))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
