from flask import escape, abort, redirect, render_template
from google.cloud import datastore
import functions_framework

datastore_client = datastore.Client()

@functions_framework.http
def submit(request):
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
        results = list(query.fetch(limit=1))

        if results:
            first_url = results[0]
            # Delete the first word
            datastore_client.delete(first_url.key)
            print(f"{first_url['url']} deleted.")
            return redirect(first_url['url'])
        else:
            # If the kind is empty
            print(f"No URLS!")        
            return 'none'
            #return redirect("https://www.google.com")
    elif request.method == 'PUT':
        return abort(403)
    else:
        return abort(405)

