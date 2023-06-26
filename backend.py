import re
from flask import Flask, jsonify, render_template
from pymongo import MongoClient

cluster_url = "mongodb.wawsrvdev108:27017"
client_pem_file = "C:\\Users\\i.duverkher\\Desktop\\important\\i.duverkher\\i.duverkher_mongo.pem"
ca_file = "C:\\Users\\i.duverkher\\Desktop\\important\\i.duverkher\\CA.pem"
auth_mechanism = "MONGODB-X509"

uri = f"mongodb://{cluster_url}/?authMechanism={auth_mechanism}&tls=true&tlsCertificateKeyFile={client_pem_file}&tlsCAFile={ca_file}"

app = Flask(__name__)


@app.route('/data', methods=['GET'])
def get_data():
    client = MongoClient(uri)

    dbase = client["diamond"]
    print(">>>>>>Connected to Diamond DB>>>>>>>>")
    collection_names = dbase.list_collection_names()
    print('List of Collection found')
    for collection_name in collection_names:
        print(f"- {collection_name}")

    collection_app_history_reason = dbase["app_history_reason"]
    count = 0
    results = []

    documentsTesting = collection_app_history_reason.find()

    for document in documentsTesting:
        key = document["_key"]
        Oid = document["_id"]
        aaData = document.get("aaData", [])
        lastAppVersion = aaData[0].get("APP_VER_INFO")
        for item in aaData:
            if item.get("APP_VER_INFO") == lastAppVersion:
                currentDate = item.get("END_DT")
                modelStatus = item.get("MDL_STATUS_NM")
                certStep = item.get("CERT_STEP_NM")

                if re.match(r"9999", currentDate) and (modelStatus in ["Request Test", "Testing", "Tested(Pass)", "Tested(Fail)"]):
                    print(key, lastAppVersion, currentDate,
                          certStep, modelStatus, Oid, sep=" ")
                    result = {
                        "AppID": key,
                        "AppVersion": lastAppVersion,
                        "CertStep": certStep,
                        "ModelStatus": modelStatus,
                        "ObjectID": Oid
                    }
                    results.append(result)
                    count += 1
                    break
            else:
                break

    client.close()

    response = {
        "total_apps": count,
        "results": results
    }

    return render_template('index.html', response=response)


if __name__ == '__main__':
    app.run()
