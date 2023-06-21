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

    collection_app_history_reason = dbase["app_history_reason"]
    # collection_version_basic_info = dbase["version_basic_info"]
    '''  queryTesting = {
            "aaData": {
                "$elemMatch": {
                    "$and": [
                        {
                            "END_DT": {"$regex": "^9999"},
                            "$or": [
                                {"CERT_STEP_NM": "Verification"},
                                {"CERT_STEP_NM": "SP Review"}
                            ]
                        }
                    ]
                }
            }
        }
    '''
    count = 0
    documentsTesting = collection_app_history_reason.find()
    # documents_version = collection_version_basic_info
    
    with open("keys.txt", "w") as file:
        print("APP_ID__________ObjectID______________Version_________________Cert Step________MDL_STATUS")

        for document in documentsTesting:
            key = document["_key"]
            Oid = document["_id"]
            aaData = document.get("aaData", [])
            appVersion = aaData[0].get("APP_VER_INFO")
            for item in aaData:
                if item.get("APP_VER_INFO") == appVersion:

                    if (re.match(r"9999", item.get("END_DT")) and (item.get("MDL_STATUS_NM") == "Request Test" or item.get("MDL_STATUS_NM") == "Testing" or item.get("MDL_STATUS_NM") == "Tested (Pass)"
                                                                   or item.get("MDL_STATUS_NM") == "Tested(Fail)")):
                        # optional conditional re.match(r"9999", item.get("END_DT")) and (item.get("CERT_STEP_NM") == "Verification" or item.get("CERT_STEP_NM") == "SP Review")
                        print(key, Oid, appVersion, item.get("END_DT"),
                              item.get("CERT_STEP_NM"), item.get("MDL_STATUS_NM"),  sep=" ")
                        file.write(
                            f"AppID:{key}, ObjectID:{Oid}, AppVersion:{appVersion} EndDate: \n")
                        count += 1
                        break
                else:
                    break

    print("Total apps count", count)
    client.close()


async def main():
    await appTestingList(client)

asyncio.run(main())
