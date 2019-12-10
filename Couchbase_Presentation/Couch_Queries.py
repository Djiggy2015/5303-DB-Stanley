from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
from couchbase.n1ql import N1QLQuery

# Connect to the cluster and buckets
cluster = Cluster('couchbase://localhost')
authenticator = PasswordAuthenticator('Admatt', 'Shadow2012')
cluster.authenticate(authenticator)
cb = cluster.open_bucket('Musicians')
cb2 = cluster.open_bucket('Albums')

# Print out the musicians who play guitar with wildcards
#for row in cb.n1ql_query("SELECT fname, lname, Instrument FROM `Musicians` WHERE Instrument LIKE '%Guitar'"):
  #print(row)

# Print Queen band members
#for row in cb.n1ql_query("SELECT fname, lname, Instrument FROM `Musicians` WHERE Band = 'Queen'"):
  #print(row)

# N1QL can work with arrays
#for row in cb2.n1ql_query("SELECT Band, Songs[1].Name AS song_name FROM `Albums`"):
  #print(row)

# You can cut off arrays
#for row in cb2.n1ql_query("SELECT Band, Name, Songs[0:3] FROM Albums WHERE Songs[0:3] IS NOT MISSING"):

#print(row)
