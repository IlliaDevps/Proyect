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


async def list_databases(client):
    databases_list = client.list_database_names()
    print("Databases found:")
    for db in databases_list:
        print(f" - {db}")

    dbase = client["diamond"]
    collection_names = dbase.list_collection_names()

    print('List of Collection found')
    for collection_name in collection_names:
        print(f"- {collection_name}")

    collection = dbase["app_history_reason"]
    query = {
        "aaData": {
            "$elemMatch": {
                "$or": [
                    {
                        "$and": [
                            {
                                "END_DT": {"$regex": "^9999"},
                                "CERT_STEP_NM": "Verification"
                            }
                        ],
                        "$and": [
                            {
                                "END_DT": {"$regex": "^9999"},
                                "CERT_STEP_NM": "SP Review"
                            }
                        ]
                    }
                ]
            }
        }
    }
    count = 0
    documents = collection.find(query)
    for document in documents:
        print(document["_key"])
        count += 1
    print(count)
    client.close()


async def main():
    await list_databases(client)

asyncio.run(main())
