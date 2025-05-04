from sanic import Sanic
from sanic_cors import CORS

app = Sanic(__name__)
CORS(app)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, workers=8, debug=False, access_log=False)

