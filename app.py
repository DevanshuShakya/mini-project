import requests
from flask import Flask,render_template,url_for
from flask import request as req

from datasets import load_dataset
import pandas as pd
from datasets import load_dataset, load_metric
from transformers import pipeline, set_seed
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

import os

from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, auth_required
from flask_security.models import fsqla_v3 as fsqla


app = Flask(__name__)
app.config['DEBUG'] = True

# Generate a nice key using secrets.token_urlsafe()
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')

# have session and remember cookie be samesite (flask/flask_login)
app.config["REMEMBER_COOKIE_SAMESITE"] = "strict"
app.config["SESSION_COOKIE_SAMESITE"] = "strict"

# Use an in-memory db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
# As of Flask-SQLAlchemy 2.4.0 it is easy to pass in options directly to the
# underlying engine. This option makes sure that DB connections from the
# pool are still valid. Important for entire application since
# many DBaaS options automatically close idle connections.
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create database connection object
db = SQLAlchemy(app)

# Define models
fsqla.FsModels.set_db_info(db)

class Role(db.Model, fsqla.FsRoleMixin):
    pass

class User(db.Model, fsqla.FsUserMixin):
    pass

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
app.security = Security(app, user_datastore)

@app.route("/",methods=["GET","POST"])
def Index():
    return render_template("new.html")

@app.route("/Summarize",methods=["GET","POST"])
def Summarize():
    if req.method== "POST":
      

        data=req.form["data"]

        maxL=int(req.form["maxL"])
        # minL=maxL//4
        # def query(payload):
        #     response = requests.post(API_URL, headers=headers, json=payload)
        #     return response.json()

        # output = query({
        #     "inputs":data,
        #     "parameters":{"min_length":minL,"max_length":maxL},
        # })[0]

        

        gen_kwargs = {"length_penalty": 0.8, "num_beams":8, "max_length": 128}

        length= len(data.split(' '))
        # print(length)

        # output= pipe(data, min_length=int((maxL* length)/100), max_length=length)[0]["summary_text"]

        # print(output['summary_text'])
        # return render_template("new.html",result=output)
    else:
        return render_template("new.html")

if __name__ == '__main__':
    
    model_name= 'pegasus-samsum-model'
    tokenizer= 'tokenizer'

    # model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(tokenizer)

    pipe = pipeline("summarization", model='pegasus-samsum-model',tokenizer=tokenizer)

    app.run()






