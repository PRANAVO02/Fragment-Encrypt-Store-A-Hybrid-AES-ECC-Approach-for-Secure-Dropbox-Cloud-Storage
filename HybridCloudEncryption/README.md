<h1>Key Generation</h1>

<b>python generate_keys.py</b>

<h1>Add token in config.py</h1>

Go to https://www.dropbox.com/developers/apps/ 
and go to the app and click the generate token, copy it, and paste it in config.py
if no app created, create an app 

ACCESS_TOKEN = "your-dropbox-access-token"

<h1>For app run</h1>

<b>python app.py</b>


<h1>For terminal run</h1>

<b>python upload.py</b>
  upload file:  give path from local

then run

<b>python download.py</b>

Now you can see the reconstructed file

<h2>*Note*</h2>

If u get any error from the Dropbox token side, the token may have expired, so go to https://www.dropbox.com/developers/apps/ 
and go to the app and click the generate token and copy it and paste it in config.py, 
it expires in 3 hrs ig


