import pymongo
from pymongo import MongoClient
def config_database():
  ##init database config
  client = MongoClient()
  client = MongoClient('localhost', 27017)
  # client = MongoClient('mongodb://localhost:27017/')
  # db = client.test_database
  # db = client['test-database']
  # print(db)

  mydb = client["mydatabase"]
  mycol = mydb["customers"]
  print(mydb.list_collection_names())
  collist = mydb.list_collection_names()
  if "customers" in collist:
    print("The collection exists.") 

def insert_data():
  mydict = { "_id": , "name": "John", "address": "Highway 37" }
  x = mycol.insert_one(mydict)
  print(x.inserted_ids)
  mydict = { "name": "John", "address": "Highway 37" }

  x = mycol.insert_one(mydict)
  print(x)
  print(mydb.list_collection_names())

  mydict = { "name": "Peter", "address": "Lowstreet 27" }

  x = mycol.insert_one(mydict)

  print(x.inserted_id)

  mylist = [
    { "_id": 1, "name": "John", "address": "Highway 37"},
    { "_id": 2, "name": "Peter", "address": "Lowstreet 27"},
    { "_id": 3, "name": "Amy", "address": "Apple st 652"},
    { "_id": 4, "name": "Hannah", "address": "Mountain 21"},
    { "_id": 5, "name": "Michael", "address": "Valley 345"},
    { "_id": 6, "name": "Sandy", "address": "Ocean blvd 2"},
    { "_id": 7, "name": "Betty", "address": "Green Grass 1"},
    { "_id": 8, "name": "Richard", "address": "Sky st 331"},
    { "_id": 9, "name": "Susan", "address": "One way 98"},
    { "_id": 10, "name": "Vicky", "address": "Yellow Garden 2"},
    { "_id": 11, "name": "Ben", "address": "Park Lane 38"},
    { "_id": 12, "name": "William", "address": "Central st 954"},
    { "_id": 13, "name": "Chuck", "address": "Main Road 989"},
    { "_id": 14, "name": "Viola", "address": "Sideway 1633"}
  ]

  x = mycol.insert_many(mylist)
  print(x.inserted_ids)

def find_data():
  x = mycol.find_one()
  print(x)

def find_all():
  for x in mycol.find():
    print(x)

def show_some_col():
  for x in mycol.find({},{ "_id": 0, "name": 1, "address": 1 }):
    print(x)
  for x in mycol.find({},{ "address": 0 }):
    print(x)

def query():
  myquery = { "address": "Park Lane 38" } 
  mydoc = mycol.find(myquery) 
  for x in mydoc:
    print(x)

  myquery = { "address": { "$gt": "S" } }  
  mydoc = mycol.find(myquery) 
  for x in mydoc:
    print(x)

  myquery = { "address": { "$regex": "^S" } } 
  mydoc = mycol.find(myquery) 
  for x in mydoc:
    print(x)

def sort_query():
  mydoc = mycol.find().sort("name", -1)
  for x in mydoc:
    print(x)

def delete_one():
  myquery = { "address": "Mountain 21" }
  mycol.delete_one(myquery)

def delete_many():
  myquery = { "address": {"$regex": "^S"} }
  x = mycol.delete_many(myquery)
  print(x.deleted_count, " documents deleted.")
  
def drop_table():
  # x = mycol.delete_many({})
  print(x.deleted_count, " documents deleted.")
  mycol.drop()

def update_one():
  myquery = { "address": "Valley 345" }
  newvalues = { "$set": { "address": "Canyon 123" } }
  mycol.update_one(myquery, newvalues)
  for x in mycol.find():
    print(x)

def update_many():
  myquery = { "address": { "$regex": "^S" } }
  newvalues = { "$set": { "name": "Minnie" } }
  x = mycol.update_many(myquery, newvalues)
  print(x.modified_count, "documents updated.")

def get_limit(): 
  myresult = mycol.find().limit(5) 
  for x in myresult:
    print(x)