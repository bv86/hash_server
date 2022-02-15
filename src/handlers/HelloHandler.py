from tornado.web import RequestHandler


class HelloHandler(RequestHandler):
    """Simple Hello world message handler"""

    def get(self):
        self.write("Hello! You can upload file to /upload")
