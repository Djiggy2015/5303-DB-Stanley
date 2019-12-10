'''
This program will upload 1 million users and their corresponding data 
to a couchbase bucket. 
'''

# will be used to generate random messages
import markovify

# allows me to connect to a cluster
from couchbase.cluster import Cluster

# allows me to access a cluster using a password authetication
from couchbase.cluster import PasswordAuthenticator 

# allows me to issue queries on the cluster
from couchbase.n1ql import N1QLQuery

# allows me to work with json-formatted data
import json

# allows me to create timestamps and track execution time of this program
from datetime import datetime
import time

# allows to generate random numbers
import random

# allows me to find the computer's ip address
import socket

def train_model():
    # Get raw text as string.
    with open("/Users/student/Desktop/1.txt", errors ="ignore") as a:
        text_a = a.read()
    with open("/Users/student/Desktop/2.txt", errors="ignore") as b:
        text_b = b.read()
    with open("/Users/student/Desktop/3.txt", errors ="ignore") as c:
        text_c = c.read()
    with open("/Users/student/Desktop/4.txt", errors="ignore") as d:
        text_d = d.read()

    # Build the models
    model_a = markovify.Text(text_a)
    model_b = markovify.Text(text_b)
    model_c = markovify.Text(text_c)
    model_d = markovify.Text(text_d)

    # Combine the models. The numbers indicate how much weight to give a particular model
    model_combo = markovify.combine([ model_a, model_b, model_c, model_d ], [ 1, 1, 1, 1 ])

    return model_combo

# generate a message and upload to database
def generate_messages(row, b_messages, b_users_messages, model, user, message_num):
    for count in range(0,message_num):
        # generate the message from trained model
        message = model.make_short_sentence(100)

        # generate a random timestamp for message
        now = int(datetime.timestamp(datetime.now()))
        timestmp = datetime.fromtimestamp(random.randint(0,now))

        # who will receive the message
        index = random.randint(0,len(row)-1)
        recipient = row[index]

        # ip address of this computer
        ipaddress = socket.gethostbyname(socket.gethostname())

        # upload database with message and connection info between sender and receiver
        b_messages.upsert(ipaddress+'::'+str(user)+'_'+str(count),{'message':message, 'create_time':str(timestmp)})
        b_users_messages.upsert(ipaddress+'::'+str(user)+'_'+str(count),{'from':user, 'to':recipient})

# open the output file
outfile = open("output.txt", 'w')

# Calculates execution time
start = time.perf_counter()

# connect to the cluster
cluster = Cluster('')
authenticator = PasswordAuthenticator('CorbinMatamoros', '')
cluster.authenticate(authenticator)

# open buckets
b_users = cluster.open_bucket('users')
b_messages = cluster.open_bucket('messages')
b_users_connections = cluster.open_bucket('user-connections')
b_users_messages = cluster.open_bucket('user-messages')

# train and return a trained model for generating random messages
model = train_model()

# This part of the program will run the queries
for user in range(0,1000000):

    # Allows us to grab a user's friend list.
    query_string1 = "select friends from `user-connections` where user_id = $1"

    # Query that will grab the user's age. The user's age will determine how
    # many messages they will send.
    query_string2 = "select age from `users` where user_id = $1"

    # Run the queries
    result1 = b_users.n1ql_query(N1QLQuery(query_string1, user))
    result2 = b_users.n1ql_query(N1QLQuery(query_string2, user))

    for row1 in result1:
        for row2 in result2:
            # number of messages sent is dependent on the age of the sender
            if (row2['age'] < 25):
                message_num = 128
            elif (row2['age'] < 35):
                message_num = 75
            elif (row2['age'] < 45):
                message_num = 52
            elif (row2['age'] < 55):
                message_num = 33
            elif (row2['age'] < 65):
                message_num = 16
            else:
                message_num = 10
            outfile.write("Individual " + str(user) + " is " + str(row2['age']) + " years old.\nThis individual will send: " + str(message_num) + " messages. ")
            generate_messages(row1["friends"], b_messages, b_users_messages, model, user, message_num)

    
execution_time = time.perf_counter() - start
print(execution_time)
