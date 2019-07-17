var map;

$(document).ready(function() {
	map = L.map('map');
	L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		attribution: '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
		maxZoom: 18,
	}).addTo(map);

//	$("#returned").hide(0)
$("#submit").click(function() {
	var postcode = $("#postcode_value").val();


	get_lat_long_postcode(postcode, function(lat, longit, height) {

		$("#mainpage").hide("slow", function() {
			$("#returned").show("slow")
		});
		map.setView([lat, longit], 13);
		// height_difference(height, avgHeight)
		// risk_rating(height_above_river)
		//s description_insert(height_above_river, postcode, number_rivers, risk_level, river_name)

		var circle = L.circle([lat, longit], 1000, {
			color: 'red',
			fillColor: '#f03',
			fillOpacity: 0.5
		}).addTo(map);

	})
	get_rivers_near(lat, longit, function() {

	})
	height_difference(height, avgHeight)
	risk_rating(height_above_river)
	description_insert(height_above_river, postcode, number_rivers, risk_level, river_name)

});

if (navigator.geolocation) {
	navigator.geolocation.getCurrentPosition(showPosition);
}
})
function get_lat_long_postcode(postcode, callback){
	$.ajax({
		method: "GET",
		url: "postcode2.json",
		data: { "postcode": postcode }
	})
	.done(function( msg ) {
		//alert( "Data Saved: " + msg );
		//alert(msg.Latitude + msg.Longitude)
		//msg = JSON.parse(msg)
		callback(msg.Latitude, msg.Longitude, msg.Height)
	});
}

function showPosition(position) {
	position.coords.latitude + position.coords.longitude
	map.setView([position.coords.latitude, position.coords.longitude], 13);
}

function get_rivers_near(lat, longit, callback){
	$.ajax({
		method: "GET",
		url: "nearbyrivers.json",
		data: {"Latitude": Latitude, "Longitude": Longitude}
	})
	.done(function( wmsg ) {
		alert( "Data Saved: " + msg );
		msg = JSON.parse(msg)
		callback(msg)
	});
}

function description_insert(height_above_river, postcode, number_rivers, risk_level, river_name) {
	$("#height_above_river").after(height_above_river)
	$("#postcode").after(postcode)
	$("#number_rivers").after(number_rivers)
	$("#risk_level").after(risk_level)
};

function height_difference(height, avgHeight) {
	var height_above_river = height - avgHeight;
}

function risk_rating(height_above_river) {
	var risk_level = ""
	if (height_above_river == -20) {
		risk_level = "Are you in Hull? Goddammit Hull!"
	}
	else if (height_above_river == -10) {
		risk_level = "very high"
	}
	else if (height_above_river == 0) {
		risk_level = "very high"
	}
	else if (height_above_river == 10) {
		risk_level = "high"
	}
	else if (height_above_river == 20) {
		risk_level = "medium"
	}
	else if (height_above_river == 30) {
		risk_level = "low"
	}
	else if (height_above_river == 40) {
		risk_level = "very low"
	}
	else if (height_above_river == 50) {
		risk_level = "negligible"
	}
}