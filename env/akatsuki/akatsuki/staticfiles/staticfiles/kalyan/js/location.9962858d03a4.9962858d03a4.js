

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
          var string = data["results"][0]["formatted_address"];
          console.log(string);
          document.getElementById("loc").value = string;
       });
}
