import logging
from tornado.web import RequestHandler
from tornado.web import stream_request_body
from streamparser import StreamingFormDataParserDelegate, StreamingFormDataParser
from constants import HTTP_BAD_REQUEST
from hashlib import sha256
from tornado.gen import coroutine


@stream_request_body
class UploadHandler(RequestHandler, StreamingFormDataParserDelegate):
    """Handler that will compute a hash for any uploaded file"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hash = None
        self.filename = None
        self.file_hashes = {}
        self.parser = None

    async def post(self):
        """In case of POST request, we return received files hashes as json"""
        if self.hash:
            self.set_status(HTTP_BAD_REQUEST)
            return self.finish({'error': {
                'code': HTTP_BAD_REQUEST,
                'message': 'Invalid multipart/form-data',
            }})
        self.write({'result': {
            'hashes': self.file_hashes
        }})

    def prepare(self):
        self.file_hashes = {}
        self.set_header('Content-Type', 'application/json')
        if self.request.method == 'POST':
            try:
                self.parser = StreamingFormDataParser(self)
            except (TypeError, ValueError):
                self.set_status(HTTP_BAD_REQUEST)
                return self.finish({'error': {
                    'code': HTTP_BAD_REQUEST,
                    'message': 'Invalid multipart/form-data',
                }})

    @coroutine
    def data_received(self, chunk: bytes):
        if self.request.method == 'POST':
            try:
                # We should be able to use await / async, but
                # the streamparser library we use was written with
                # non native coroutines
                yield self.parser.data_received(chunk)
            except Exception:
                self.set_status(HTTP_BAD_REQUEST)
                return self.finish({'error': {
                    'code': HTTP_BAD_REQUEST,
                    'message': 'Invalid multipart/form-data',
                }})

    def start_file(self, headers, disp_params):
        # Handle key values the same we as we handle files
        self.filename = disp_params.get(
            'filename', disp_params.get('name', None))

        if self.hash:
            self.set_status(HTTP_BAD_REQUEST)
            return self.finish({'error': {
                'code': HTTP_BAD_REQUEST,
                'message': 'Invalid multipart/form-data',
            }})

        self.hash = sha256()

    def finish_file(self):
        if not self.hash or not self.filename:
            logging.error(
                'No hash context available, invalid multipart/form-data')
            return
        self.file_hashes[self.filename] = self.hash.hexdigest()
        self.hash = None
        self.filename = None

    def file_data_received(self, file_data):
        self.hash.update(file_data)
