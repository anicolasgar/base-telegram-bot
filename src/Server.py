import os

from flask import Flask

app = Flask(__name__)


class Server:
    @app.route('/compute/<operation>')
    def compute(self, operation):
        if not operation.args:
            return "Invalid argument"
        return "Executed operation: " + operation.args[0]


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5050))
    app.run(debug=True, host='0.0.0.0', port=port)
