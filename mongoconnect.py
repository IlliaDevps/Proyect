from pymongo import MongoClient

cluster_url = "mongodb.wawsrvdev108:27017"
client_pem_file = ".\\ssl\\i.duverkher_mongo.pem"
ca_file = ".\\ssl\\CA.pem"
auth_mechanism = "MONGODB-X509"

uri = f"mongodb://{cluster_url}/?authMechanism={auth_mechanism}&tls=true&tlsCertificateKeyFile={client_pem_file}&tlsCAFile={ca_file}"

# Create a new MongoClient
client = MongoClient(uri)

# Function to connect to the server and gather data
async def run():
    try:
        print("--------------------------------------------------------------")
        # Connect the client to the server
        await client.connect()
        # Database
        diamond_db = client.diamond
        # Establish and verify connection
        await client.admin.command("ping")
        print("Connected to database")
        await list_databases(client)
        print("--------------------------------------------------------------")
    except Exception as e:
        print(e)
    finally:
        # Ensure that the client will close when you finish/error
        await client.close()

async def list_databases(client):
    databases_list = await client.list_database_names()
    print("Databases found:")
    for db in databases_list:
        print(f" - {db}")

await run()
