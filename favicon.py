from flask import Flask, send_file, request

from favicon_extractor.favicon_extractor import get_favicon, download_or_create_favicon

import socket
import os

app = Flask(__name__)

MEDIA_ROOT='{}/icons'.format(os.path.dirname(os.path.realpath(__file__)))


@app.route("/")
def grab_favicon():
    domain  = request.args.get('domain', None)
    refresh = request.args.get('refresh', None)

    if domain is None:
        return 'No domain given'

    domain = domain.split('?')[0].split('/')[0]

    # resolve DNS on domain
    try:
        socket.gethostbyname(domain)
    except socket.error:
        return 'DNS or other network error for {}'.format(domain)

    # TODO: check that file exists on file system
    filename = '{}/{}.png'.format(MEDIA_ROOT, domain)
    if not os.path.isfile(filename) or refresh:
        favicon = get_favicon(domain)
        img = download_or_create_favicon(favicon, domain)
        img.save(filename)

    return send_file(filename, mimetype='image/png')


    


if __name__ == "__main__":
    app.debug = True
    app.run()
