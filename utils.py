import firebase_admin
from firebase_admin import credentials
from firebase_admin import db



cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
  'databaseURL': 'https://spoken-2e7a4.firebaseio.com/'
}, name='spoken')


# Function that reads from firebase realtime database 
def database_read(node):

  # Get the reference to the node in a database, root node: /
  ref = db.reference(node, app=firebase_admin.get_app(name='spoken'))
  # Read data from the node, snapshot is a dictionary
  snapshot = ref.order_by_key().get()
  # Format data
  output=list(snapshot.items())
  output.sort(reverse=True) 
  return output