from flask import escape, abort, redirect, render_template
from google.cloud import datastore

import functions_framework
import re

datastore_client = datastore.Client()

@functions_framework.http
def submit(request):
    print("#### Received Form ")

    query = datastore_client.query(kind="urls")
    entities = list(query.fetch())
    for entity in entities:
        print(f"Deleting {entity.key}")
        datastore_client.delete(entity.key)

    key = datastore_client.key("urls")
    print("Created a key")

    formurls = request.form['urlfile']
    urls = formurls.split()
    for url in urls:
        print("Writing URL " + url)
        urlent = datastore.Entity(key)
        urlent['url'] = url
        datastore_client.put(urlent)    

    return "done"

#@functions_framework.http
def upload(request):
    return render_template('index.html')

@functions_framework.http
def main(request):

    if request.method == 'GET':

        query = datastore_client.query(kind="urls")
        # Fetch the first entity
        first_word = list(query.fetch(limit=1))

        if first_word:
            first_word = first_word[0]
            # Delete the first word
            datastore_client.delete(first_word.key)
            print(f"{first_word['url']} deleted.")
            return first_word['url']
        else:
            # If the kind is empty
            print(f"No URLS!")        
            return 'none'
            #return redirect("https://www.google.com")
    elif request.method == 'PUT':
        return abort(403)
    else:
        return abort(405)

#app = Flask(__name__)

#@app.route('/')
#def redirect_url():
#    return redirect("https://www.google.com")
