#!/usr/bin/env python
"""
QR Code Generator home page route.
"""
from flask import Blueprint, render_template


views = Blueprint('views', __name__, url_prefix='/views')

@views.route('/', methods=['GET'])
def home():
    return render_template('home.html')
    #return 'Welcome to KSUBEB STAFF DATA BACE!'