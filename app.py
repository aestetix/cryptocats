#!flask/bin/python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import send_file
from flask import request
from flask import make_response
import re
import gnupg
import urllib.parse
import os, random
import json

gpg = gnupg.GPG(gnupghome='/home/gpgfs/data/.gnupg')

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home/gpgfs/gpg.db"
db = SQLAlchemy(app)

class GPGKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fingerprint = db.Column(db.String, unique=True)
    uploaded = db.Column(db.Boolean)

@app.route('/cat.js')
def gpgjs():
    return send_file('cat.js')

@app.route('/cryptocats.png')
def cryptocats():
    return send_file('cryptocats.png')

@app.route('/favicon.ico')
def favicon():
    return send_file('favicon.ico')

@app.route('/')
@app.route('/index.html')
def indexhtml():
    return send_file('index.html')

@app.route('/ccpa-privacy.html')
def ccpa():
    return send_file('ccpa-privacy.html')

@app.route('/getnewkey')
def index():
    global gpg
    key = db.session.query(GPGKey.fingerprint).filter(GPGKey.uploaded== None ).first()
    key_exporter = gpg.export_keys(key[0])

    # turn it into something we can upload
    key_upload = urllib.parse.quote(str(key_exporter))
    url_upload = fetch_keyserver()
    newkey = {'key': key_upload, 'keyserver': url_upload, 'fingerprint': key[0] }

    return json.dumps(newkey)

@app.route('/cat.jpg')
def cat():
    photo = random.choice(os.listdir("/home/gpgfs/data/catfolder/"))
    resp = make_response(send_file('/home/gpgfs/data/catfolder/'+photo, mimetype='image/jpg'))
    resp.headers['Cache-Control'] = "no-store"
    return resp

@app.route('/markusedkey')
def markusedkey():
    fingerprint = request.args.get('key')
    if (not re.match("^[A-Fa-f0-9]{40}$",fingerprint)):
        return ""
    elif (db.session.query(GPGKey.fingerprint).first() == None):
        return ""
    else:
        sql = "update gpg_key set uploaded = True where fingerprint = '" + fingerprint + "';"
        db.engine.execute(sql)
    return ""

def fetch_keyserver():
    lines = open('keyservers').read().splitlines()
    myline = random.choice(lines)
    return myline

if __name__ == '__main__':
    app.run(host='0.0.0.0')
