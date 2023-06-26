import re
import asyncio
from pymongo import MongoClient

cluster_url = "mongodb.wawsrvdev108:27017"
client_pem_file = "C:\\Users\\i.duverkher\\Desktop\\important\\i.duverkher\\i.duverkher_mongo.pem"
ca_file = "C:\\Users\\i.duverkher\\Desktop\\important\\i.duverkher\\CA.pem"
auth_mechanism = "MONGODB-X509"

uri = f"mongodb://{cluster_url}/?authMechanism={auth_mechanism}&tls=true&tlsCertificateKeyFile={client_pem_file}&tlsCAFile={ca_file}"

# Create a new MongoClient
print("--------------------------Creating a new MongoClient------------------------------------")
client = MongoClient(uri)

# Function to connect to the server and gather data


async def appTestingList(client):
    databases_list = client.list_database_names()
    print("Databases found:")
    for db in databases_list:
        print(f" - {db}")

    dbase = client["diamond"]
    collection_names = dbase.list_collection_names()

    print('List of Collection found')
    for collection_name in collection_names:
        print(f"- {collection_name}")

    collection_verification_test = dbase["verification_tests"]
    query = {'TEST_STAT_NM': 'Testing'}
    sort = [('REQ_DT', -1)]

    count = 0
    documentsTesting = collection_verification_test.find(query).sort(sort)
    # documents_version = collection_version_basic_info
    documentAppIDList = []
    documentUniqueID = []
    with open("keys.txt", "w") as file:
        print("APP_ID________Version____TesterName")

        for document in documentsTesting:

            appID = document["APP_ID"]
            # print(appID)
            appVersion = document["APP_VER_INFO"]
            testername = document["TESTER_NM"]
            if appID not in documentAppIDList:
                documentAppIDList.append(document["APP_ID"])
                documentUniqueID.append(document)
                print(appID, appVersion, testername, sep=" ")
                file.write(
                    f"AppID  :{appID}, AppVersion  : {appVersion}, Testername  : {testername}  \n")
                count += 1

    print("Total apps count", count)
    client.close()


async def main():
    await appTestingList(client)

asyncio.run(main())
