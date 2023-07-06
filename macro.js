
var backendUrl = "http://106.120.70.108:5000";
var script = document.createElement('script');
script.src = 'https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js';
script.onload = runAxiosRequest;
document.head.appendChild(script);

const headers = {
  "Accept": "application/json"
};

function runAxiosRequest() {
  axios.get(url, {
    headers: headers,
    httpsAgent: {
      rejectUnauthorized: false
    }
  })
    .then(function(response) {
      console.log(JSON.stringify(response.data, null, 4));
    })
    .catch(function(error) {
      console.error("Error:", error.message);
    });
}

// Include Axios library from CDN


/*const page_id = "560881462";
const url = `https://kb.sprc.samsung.pl/rest/api/content/${page_id}`;

const auth = {
  username: "i.duverkher",
  password: "4i8c66j5q2o344ercc7kmlrq0u9mofq"
};

const headers = {
  "Accept": "application/json"
};

function runAxiosRequest() {
  axios.get(url, {
    auth: auth,
    headers: headers,
    httpsAgent: {
      rejectUnauthorized: false
    }
  })
    .then(function(response) {
      console.log(JSON.stringify(response.data, null, 4));
    })
    .catch(function(error) {
      console.error("Error:", error.message);
    });
}

// Include Axios library from CDN
var script = document.createElement('script');
script.src = 'https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js';
script.onload = runAxiosRequest;
document.head.appendChild(script);*/



