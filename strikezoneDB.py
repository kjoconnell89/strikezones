import pymongo

szClient = pymongo.MongoClient('mongodb://localhost:27017/')

strikezoneDB = szClient['strikezones']
testingTBL = strikezoneDB['testing']

#testingTBL.insert_one({'test': 'bye'})
#testingTBL.insert_many([{'test': 'bye'}, {'test': 'k'}])

print(szClient.list_database_names())
print(strikezoneDB.list_collection_names())
for x in testingTBL.find():
    print(x)