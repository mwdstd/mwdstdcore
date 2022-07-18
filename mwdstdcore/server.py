from flask import Flask, jsonify, make_response
from mwdstdcore.api.v1 import api as apiv1


app = Flask(__name__)


@app.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


app.register_blueprint(apiv1, url_prefix='/v1')

if __name__ == '__main__':
    app.run(debug=True)
