function getLocation() {
    if (navigator.geolocation) {
        return
        {
        	"Latitude": position.coords.latitude,
        	"Longitude": position.coords.longitude
        };
    } else {
        return false;
    }
}
function pos(){
	var location = getLocation();
    if(location === false)
    {
        document.login.location.value="Location not available"
    }
    else
    {
        console.log(location);
        $.getJSON("https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=AIzaSyCPy4FDC0ZtO9Ci7vroeIxrzkll4euPYuEY", function(data){
        alert(data);
        });
    }
}