# store standard routes for app (login will be in autgh.py)
import sys
import os
from flask import Blueprint, render_template, jsonify

# Add path to connector.py
sys.path.append(os.path.join(os.path.dirname(__file__), '../python database functions'))
from connector import view_censored_customer_data

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/api/customers')
def api_customers():
    cols_query = ['customerFirst','customerLast','address','balance','creditScore','bankNumR','bankNumA','SSN']
    results = view_censored_customer_data(cols_query)

    
    return jsonify(results)
