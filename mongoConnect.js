import pkg from 'mongodb';
const { MongoClient } = pkg;

const clusterUrl = "mongodb.wawsrvdev108:27017";
const clientPEMFile = encodeURIComponent(".\\ssl\\i.duverkher_mongo.pem");
const caFile = encodeURIComponent(".\\ssl\\CA.pem");
const authMechanism = "MONGODB-X509";

const uri =
    `mongodb://${clusterUrl}/?authMechanism=${authMechanism}&tls=true&tlsCertificateKeyFile=${clientPEMFile}&tlsCAFile=${caFile}`;

// Create a new MongoClient
const client = new MongoClient(uri, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

// Function to connect to the server and data gathering
async function run() {
    try {
        console.log("--------------------------------------------------------------")
        // Connect the client to the server
        await client.connect();
        // database
        const diamondDb = client.db("diamond");
        // Establish and verify connection
        await client.db("admin").command({ ping: 1 });
        console.log("Connected to database");
        await listDatabases(client);
        console.log("--------------------------------------------------------------")
    } catch (e) {
        console.error(e);
    } finally {
        // Ensures that the client will close when you finish/error
        await client.close();
    }
}

run()

async function listDatabases(client) {
    var databasesList = await client.db().admin().listDatabases();
    console.log("Databases found: ");
    databasesList.databases.forEach(db => console.log(` - ${db.name}`));
};