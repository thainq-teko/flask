from flask import Flask
from flask_cors import CORS

app = Flask('TekoTrainingModule')
app.debug = True
CORS(app)


from TekoTrainingModule.controllers import *
