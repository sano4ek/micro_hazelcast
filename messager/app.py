
from flask import Flask

app = Flask(__name__)


@app.route('/messenger')
def messenger():
    return 'Not implemented yet.'


if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8089, debug=True)

