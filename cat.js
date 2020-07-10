var url = 'https://www.cryptocats.me/getnewkey';
var confirmurl = 'https://www.cryptocats.me/markusedkey';
var catphoto = document.createElement("img");
var keyfingerprint = "";
catphoto.setAttribute("src","https://www.cryptocats.me/cat.jpg");
catphoto.setAttribute("class","img-fluid");

var result = fetch(url, {
   method: 'get',
  }).then(function(response) {
    return response.json();
  }).then(function(data) {
    var key = data.key;
    var keyserver = data.keyserver;
    keyfingerprint = data.fingerprint;
    var keybody = key.replace(/\%20/g,"+");
    var keybody = "keytext=" + keybody.replace(/\%0A/g,"\%0D\%0A");
    var newurl = keyserver + "/pks/add";
    return fetch(newurl, {
	    method: 'POST',
	    headers: {
		    'Host': keyserver,
		    'Content-Type': 'application/x-www-form-urlencoded'
            },
	    body: keybody
        })
  }).then(function(response) {
    if (response.status == 200) {
      document.getElementById('cat').appendChild(catphoto);
      return fetch(confirmurl+"?key="+keyfingerprint);
    }
  });
