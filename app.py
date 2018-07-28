import os

from flask import Flask, json, request, send_from_directory, current_app
from flask_cors import CORS
from flask_jwt import JWT, timedelta
from flask_restful import Api
from apiResponse import *
from Jzon import jsonify
from Model import Model
from classifier.Classifier import Classifier

from werkzeug import secure_filename

# ========================================
#              API SETUP
# ========================================
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)
version = 1
baseResource = "/api/v" + str(version)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = "C:\\Users\\Migue\\Documents\\Data"
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=86400)
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

classifier = None

# ========================================
#              API ROUTES
# ========================================


@app.route('/', methods=['GET'])
def index():
    return current_app.send_static_file('index.html')


@app.route('/<path:path>', methods=['GET'])
def index2(path):
    try:
        return current_app.send_static_file(path)
    except Exception as identifier:
        return current_app.send_static_file('index.html')


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(
        ['jpg', 'jpeg', 'png'])
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def parseFileName(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    res = "tempimage" + "." + ext
    return res


@app.route('/api/classify', methods=['POST'])
def upload():
    # check if the post request has the file part
    file = request.files['file']
    if (file and allowed_file(file.filename)):
        filename = parseFileName(file.filename)

        filename = secure_filename(filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'] + "\\temp", "")
        try:
            os.stat(path)
        except:
            os.mkdir(path)

        path = path  + filename     
        file.save(path)
        try:
            resp = classifier.classify(path)
            return Ok(resp)
        except Exception as identifier:
            return BadRequest()
    return BadRequest()

# ========================================
#              API START UP
# ========================================
if __name__ == '__main__':
    env = 'dev'  # dev, debug, prod
    global classifier
    classifier = Classifier()
    if(env == 'dev'):
        app.run(debug=True)
    elif (env == 'debug'):
        app.run(debug=False)
    elif(env == 'prod'):
        # Docker production configuration
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port)
