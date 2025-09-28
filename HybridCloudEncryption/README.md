<h1>Key Generation</h1>

python generate_keys.py

<h1>Add token in config.py</h1>
Go to https://www.dropbox.com/developers/apps/ 
and go to the app and click the generate token, copy it, and paste it in config.py

ACCESS_TOKEN = "your-dropbox-access-token"

<h1>For app run</h1>

python app.py


<h1>For terminal run</h1>

python upload.py
  upload file:  give path from local

then run

python download.py

Now you can see the reconstructed file

<h2>*Note*</h2>

If u get any error from Dropbox token side, the token may have expired so go to https://www.dropbox.com/developers/apps/ 
and go to the app and click the generate token and copy it and paste it in config.py, 
it expires in 3 hrs ig

