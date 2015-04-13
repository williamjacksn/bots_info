import flask
import hashlib

app = flask.Flask(__name__)
cache = dict()
etags = dict()


@app.route('/')
def index():
    if flask.request.path in etags:
        etag = etags.get(flask.request.path)
        if 'if-none-match' in flask.request.headers:
            req_etag = flask.request.headers.get('if-none-match')
            if etag == req_etag:
                return flask.Response(status=304)
    if flask.request.path in cache:
        return cache.get(flask.request.path)
    template = flask.render_template('index.html')
    response = flask.make_response(template)
    etag = hashlib.md5(template.encode()).hexdigest()
    etags[flask.request.path] = etag
    response.headers['ETag'] = etag
    return cache.setdefault(flask.request.path, response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
