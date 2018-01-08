from googletrans import Translator
import http.server
import socketserver
import json
import urllib.request
import sys

translator = Translator(service_urls=[
      'translate.google.ro'
    ])

def get_matches(word):

    request_str = "http://api.datamuse.com/words?sl={}".format(word)
    request = urllib.request.urlopen(request_str).read()
    response = json.loads(request.decode('UTF-8'))
    if len(response) == 0:
        return []

    return [x["word"] for x in response]

def translate(words, target_lang):
    if len(words) == 0:
        return []
    translations = None
    try:
        translations = translator.translate(words, dest=target_lang)
    except Exception as exc:
        print(exc)
    if 0 == len(translations):
        return []
    return [translation.text for translation in translations]

def match_word(word):
    translations_in_english = translate([word], 'en')

    if len(translations_in_english) == 0:
        return  None
    translated_in_english = translations_in_english[0]

    if translated_in_english is None:
        return None

    matches = get_matches(translated_in_english)
    if len(matches) == 0:
        return None

    for match in matches:
        translations = translate([match], 'ro')
        for translation in translations:
            if word == translation:
                continue
            return translation

    return None

class Server(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):

        content_len = int(self.headers['content-length'])
        post_body = self.rfile.read(content_len)

        try:
            request = json.loads(post_body.decode("UTF-8"))

            words = None
            try:
                words = request["words"]
            except Exception as ex:
                self.send_response(400, 'Bad Request')
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes('{"error" : "words node is missing"}', 'UTF-8'))
                return

            if not isinstance(words, list):
                self.send_response(400, 'Bad Request')
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes('{"error" : "words node must be of type list"}', 'UTF-8'))
                return

            for word in words:
                if not isinstance(word, str):
                    self.send_response(400, 'Bad Request')
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(
                        bytes('{"error" : "words node can only contain string objects"}', 'UTF-8'))
                    return

            response = {}
            matched = []
            not_matched = []

            for word in words:
                match = match_word(word)
                if match is None:
                    not_matched.append(word)
                else:
                    matched.append(match)

            response["matched"] = matched
            response["not-matched"] = not_matched

            self.send_response(200, 'OK')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response), 'UTF-8'))

        except Exception as exc:
            print("Exception in request\nPost body: {0}\nException: {1}".format(post_body, exc))

    def serve_forever(address, port):
        socketserver.TCPServer((address, port), Server).serve_forever()
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Ussage: server.py [address] [port]")
        exit(1)
    Server.serve_forever(sys.argv[1], int(sys.argv[2]))
