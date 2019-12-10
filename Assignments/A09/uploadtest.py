'''
This program is a test to see how uploading a large
amount of data to couchbase will turn out. This 
program uploads only a thousand users to a bucket.
The final version will upload one million.
'''

from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
from couchbase.n1ql import N1QLQuery
import json

# Connect to the cluster and buckets
cluster = Cluster('couchbase://localhost')
authenticator = PasswordAuthenticator('Admatt', '')
cluster.authenticate(authenticator)
cb = cluster.open_bucket('Matt_Users')

documentname = " "
id = 0
username = " "
email = " "
fname = " "
lname = " "
password = " "

with open('Users.json', 'r') as myfile:
  data = myfile.read()

obj = json.loads(data)

for x in range(0, 1000):
  documentname = "user " + str(x + 1)

  id = obj[x]['user_id']
  username = obj[x]['username']
  email = obj[x]['email']
  fname = obj[x]['first_name']
  lname = obj[x]['last_name']
  password = obj[x]['password']
  create_time = obj[x]["create_time"]
  last_update = obj[x]["last_update"]


  cb.insert(documentname, {"id":id,"username":username,"email":email,"first_name":
  fname,"last_name":lname,"password":password, "create_time": create_time, 
  "last_update": last_update})
