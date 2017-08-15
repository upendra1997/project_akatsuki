function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(pos);
    } else { 
        return false;
    }
}

function pos(position){
       //todo
       var val = '';
       $.getJSON("https://maps.googleapis.com/maps/api/geocode/json?latlng="+position.coords.latitude+","+position.coords.longitude+"&key=AIzaSyCPy4FDC0ZtO9Ci7vroeIxrzkll4euPYuE", function(data) {
            var string = data["results"][0]["formatted_address"]
            val = string;
       });
       return val;
}