import json

from rest_framework import parsers


class StreamParser(parsers.BaseParser):
    media_type = 'application/stream-json'

    def parse(self, stream, media_type=None, parser_context=None):
        data = []
        for chunk in stream:
            chunk_data = chunk.decode('utf-8').strip()
            if chunk_data == "END":
                break
            data.append(json.loads(chunk_data))
        return data