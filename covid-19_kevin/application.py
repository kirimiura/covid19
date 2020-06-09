import os
from flask import Flask, session, render_template, request, redirect, jsonify, url_for
from flask_session import Session

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import requests

import pandas as pd
import pickle
import collections

app = Flask(__name__)

df_covid = pickle.load(open("./df.p", "rb"))
X = pickle.load(open("./X_embedded.p", "rb"))
# 2D embedding of X from t-SNE
#X_embedded = pickle.load(open("./X_embedded.p", "rb"))
#  Labels produced by k-means
#y_pred = pickle.load(open("./y_pred.p", "rb"))

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search",methods=["POST"])
def search():
    word = request.form.get("word")
    searched = df_covid["abstract"].str.contains(word)
    
    c = collections.Counter(list(df_covid[searched]["y"]))
    most_hit_y = c.most_common()[0][0]
    df = df_covid[df_covid["y"]==most_hit_y]

    n = 5
    literatures = []
    for i in range(n):
        l_1 = df.iloc[i,[0,2,4,5]].to_dict()
        literatures.append(l_1)

    #l1 = df.iloc[0,[0,2,4,5]].to_dict()
    #l2 = df.iloc[1,[0,2,4,5]].to_dict()
    #l3 = df.iloc[2,[0,2,4,5]].to_dict()

    return render_template("literature.html",word=word,literatures=literatures)


@app.route("/search_form/<string:paper_id>")
def search_form(paper_id):
    #paper_id = request.form.get("paper_id")
    #df = df_covid[df_covid["paper_id"]==paper_id]
    center_num = 0
    for i in range(len(X)):
        if df_covid.iloc[i,0] == paper_id:
            center_num = i
            break
    
    x = X.iloc[center_num,0]
    y = X.iloc[center_num,1]

    lengths = []
    for i in range(len(X)):
        x_1 = X.iloc[i,0]
        y_1 = X.iloc[i,1]
        length = (x-x_1)**2 + (y-y_1)**2
        lengths.append([length,i])
    lengths.sort()

    n = 10
    literatures = []
    for i in range(n):
        id_1 = df_covid.iloc[lengths[i][1],0]
        l_1 = df_covid[df_covid["paper_id"]==id_1].iloc[0,[0,2,4,5]].to_dict()
        literatures.append(l_1)
        
    return render_template("literature.html", literatures=literatures)