import random
from flask import Flask, abort, request, render_template, redirect, jsonify
from sqlite3 import OperationalError
import string
import sqlite3
from dotenv import load_dotenv
import os
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


load_dotenv()

#Assuming urls.db is in your app root folder
app = Flask(__name__)
app_name = 'url-short'

HOST = os.getenv("HOST")
DATABASE_NAME = os.getenv('DATABASE_NAME')
SHORT_CODE_LENGTH = os.getenv('SHORT_CODE_LENGTH')
TABLE_NAME = 'WEB_URL'

def table_check():
    create_table = """CREATE TABLE WEB_URL(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        original_url TEXT NOT NULL,
        url_prefix TEXT NOT NULL,
        short_code TEXT NOT NULL
        );
        """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(create_table)
        except OperationalError as e:
            logger.error("Error while creating table due to %s",str(e))


def insert_short_code_db(original_url, url_prefix, short_code):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        insert_row = f"INSERT INTO {TABLE_NAME} (original_url, url_prefix, short_code) VALUES (?, ?, ?)"
        cursor.execute(insert_row,(original_url,url_prefix,short_code))

def create_short_code(url_prefix):
    characters = string.ascii_letters + string.digits
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        result=None
        while True:
            short_code = ''.join(random.choice(characters) for _ in range(6))

            result = cursor.execute(f'SELECT id FROM {TABLE_NAME} WHERE url_prefix = ? AND short_code = ?',(url_prefix,short_code)).fetchone()
            if result is None:
                return short_code
            
def get_existing_url(url_prefix, original_url):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        query = f"SELECT short_code FROM {TABLE_NAME} WHERE url_prefix = ? AND original_url = ?"
        result = cursor.execute(query, (url_prefix, original_url)).fetchone()
    return result[0] if result else None



def check_url_scheme(original_url):
    if urlparse(original_url).scheme == '':
        original_url = 'http://' + original_url
    return original_url

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url_prefix = request.form.get('url_prefix',"s")
        original_url = check_url_scheme(request.form.get('url'))
        existing_short_code = get_existing_url(url_prefix,original_url)
        if existing_short_code:
            short_code =  existing_short_code
        else:
            short_code = create_short_code(url_prefix)
            insert_short_code_db(original_url, url_prefix, short_code)
        return render_template('home.html',short_url= "/".join([HOST,url_prefix,short_code]))
    return render_template('home.html')



@app.route('/<url_prefix>/<short_code>')
def redirect_short_url(url_prefix,short_code):
    redirect_url = None
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        select_row = f'SELECT original_url FROM {TABLE_NAME} WHERE url_prefix = ? AND short_code = ?'
        try:
            redirect_url = cursor.execute(select_row,(url_prefix,short_code)).fetchone()[0]
        except IndexError:
            logger.error("url not found for url prefix %s, short code %s",url_prefix,short_code)
    if not redirect_url:
        abort(404)
    return redirect(redirect_url)


#API for third party call
@app.route('/v1/url/short', methods=['GET', 'POST'])
def url_short():
    if request.method == 'POST':
        url_prefix = request.json.get('url_prefix',"short")
        original_url = check_url_scheme(request.json.get('url'))
        existing_short_code = get_existing_url(url_prefix,original_url)
        if existing_short_code:
            short_code =  existing_short_code
        else:
            short_code = create_short_code(url_prefix)
            insert_short_code_db(original_url, url_prefix, short_code)
        return jsonify(
            {
                "short_url": "/".join([HOST,url_prefix,short_code])
            }
        )


if __name__ == '__main__':
    # This code checks whether database table is created or not
    table_check()
    app.run(debug=True)