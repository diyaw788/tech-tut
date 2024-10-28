# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Import core packages
import os

# Import Flask 
from flask import Flask
import pymysql

# Inject Flask magic
app = Flask(__name__)
app.secret_key = "12345678abcdefg"

dbConn = pymysql.connect(
    host="office.scholars.bond",
    port=3309,
    user='bit4444group20',
    password='CGw7f2[?4/mx',
    database='bit4444group20',
    cursorclass=pymysql.cursors.DictCursor
)

cursor=dbConn.cursor()


# Import routing to render the pages
from app import views
