
// function pos(position){
//        //todo
//        var val = '';
//         console.log("hruwfj");
//        $.getJSON("https://maps.googleapis.com/maps/api/geocode/json?latlng="+position.coords.latitude+","+position.coords.longitude+"&key=AIzaSyCPy4FDC0ZtO9Ci7vroeIxrzkll4euPYuE", function(data) {
//             var string = data["results"][0]["formatted_address"]
//             val = string;
//             console.log("hruwafafqafe");
//        });
//        console.log(val);
// }

// function getLocation(callback) {
//     if (navigator.geolocation) {
//         navigator.geolocation.getCurrentPosition(pos);
//         callback();
//         return true;
//     } else { 
//         return false;
//     }
// }

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(pos);
    } else { 
        //do nothing
    }
}

function pos(position){
       //todo
       $.getJSON("https://maps.googleapis.com/maps/api/geocode/json?latlng="+position.coords.latitude+","+position.coords.longitude+"&key=AIzaSyCPy4FDC0ZtO9Ci7vroeIxrzkll4euPYuE", function(data) {
          var string = data["results"][0]["formatted_address"]
          document.getElementById("loc").value = string;
       });
}