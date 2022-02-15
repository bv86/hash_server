from tornado.ioloop import IOLoop
from tornado.web import Application
import argparse
from handlers import *


def make_app():
    return Application([
        (r"/", HelloHandler),
    ])


def _main():
    """Web server entry point when run from command line"""
    parser = argparse.ArgumentParser(
        description='Webserver written with Tornado')
    parser.add_argument('--port')
    args = parser.parse_args()
    port = args.port or 8888
    app = make_app()
    app.listen(port)
    IOLoop.current().start()


if __name__ == "__main__":
    _main()
