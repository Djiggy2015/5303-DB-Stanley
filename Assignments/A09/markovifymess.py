'''
This program plays around with the Markovify library
in order to create some random messages and then uploads
them into a couchbase bucket.
'''

import markovify
import json
from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
from couchbase.n1ql import N1QLQuery


cluster = Cluster('couchbase://localhost')
authenticator = PasswordAuthenticator('Admatt', 'BO120MAC')
cluster.authenticate(authenticator)
cb = cluster.open_bucket('Matt_Messages')

# Used to group the messages 
id = 0
timestamp = " "
message = " "

with open("time1.json", 'r') as myfile:
  time = myfile.read()

obj = json.loads(time)

# Get raw text as string
with open("Adventures_of_Sherlock_Holmes.txt", encoding = 'utf-8') as f:
  text_a = f.read()

#Build a model
model_a = markovify.Text(text_a)


with open("alice.txt", encoding = 'utf-8') as f2:
  text_b = f2.read()

model_b = markovify.Text(text_b)

# Combine the models
model_both = markovify.combine([model_a, model_b], [1, 1])

#Print some randomly-generated sentences
for i in range(0, 1000):
  documentname = "Message " + str(i + 1)
  sentence = model_both.make_sentence()

  id = obj[i]['id']
  timestamp = obj[i]["timestamp"]
  message = sentence

  # Upload the message into the couchbase bucket
  cb.insert(documentname, {"id":id, "timestamp": timestamp, "message": message})
