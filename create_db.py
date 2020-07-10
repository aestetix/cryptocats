#!/bin/python3
import struct
import gnupg
import base64
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

gpg = gnupg.GPG(gnupghome='/home/gpgfs/data/.gnupg')
f = open('/home/gpgfs/data/blocks.tar.gz', 'rb+')
counter = 0

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home/gpgfs/gpg.db"
db = SQLAlchemy(app)


class GPGKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fingerprint = db.Column(db.String, unique=True)
    uploaded = db.Column(db.Boolean)

db.create_all()

def create_key(name):
    global gpg
    input_data = gpg.gen_key_input(
        key_type='RSA',
        key_length=1024,
        name_real='PGP File System',
        name_comment=name,
        name_email='placeholder@email.address',
        passphrase='my passphrase'
    )
    key = gpg.gen_key(input_data)
    return key

while counter < 99999999999:
    f.seek(counter*750)
    x = f.read(750)
    key = create_key(base64.b64encode(x))
    db.session.add(GPGKey(fingerprint=key.fingerprint))
    db.session.commit()
    counter = counter + 1
