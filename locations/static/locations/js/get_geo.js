function get_geo()
{
	var addr = document.getElementById('_addr').value
	var city = document.getElementById('_city').value
	var state = document.getElementById('_state').value
	alert('addr=',addr)
	alert('city=',city)
	alert('state=',state)
	if (addr != "" & city != "" & state != "")
	{
		let requestURL = 'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address=2+Palm Pl+W.+Babylon+NY&benchmark=9&format=json';
		let request = new XMLHttpRequest();
		request.open('GET', requestURL);
		request.responseType = 'json';
		request.send()
		
		request.onload = function() {
		const locationResp = request.response;
		var res = JSON.parse(locationResp)
		var zip_code = res.suffixQualifier.zip
		var lat = res.coordinates.x
		var lng = res.coordinates.y
		alert('zip_code=',zip_code)
		alert('lat=',lat)
		alert('lng=',lng)
		
		document.getElementById('_zip').value = zip_code;
		document.getElementById('_lat').value = lat;
		document.getElementById('_lng').value = lng;
		
		}
	}
}
		
		
	
	
