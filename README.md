## Your own DIY POAP dispenser

Setting up your GCP environment and enabling Cloud Datastore is out of scope

Deploy the three endpoints
```
$ gcloud functions deploy main --runtime python310 --trigger-http --allow-unauthenticated
$ gcloud functions deploy submit --runtime python310 --trigger-http --allow-unauthenticated
$ gcloud functions deploy upload --runtime python310 --trigger-http --allow-unauthenticated
```

Visit /upload and paste in the URLs from your POAP email

Use the /main URL in a QR code generator or written to an NFC tag

It will pull a URL from the datastore, delete it and then redirect the browser
