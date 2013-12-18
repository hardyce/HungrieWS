jQuery.ajaxSetup({ 
  'beforeSend': function(xhr) {xhr.setRequestHeader("Accept", "text/javascript")} 
})


// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

$(document).ready(function(){
	 $('#address_window').hide();
	 $('#notification_window').hide();
	 $('#order_info_window').hide();
	 $('#order_window').hide();
	 
});

function getJSON(url, callback){
$.ajax({
	 beforeSend: function(xhrObj){
	xhrObj.setRequestHeader("Content-Type","application/json");
	xhrObj.setRequestHeader("Accept","application/json");
	xhrObj.setRequestHeader("X-CSRFToken", csrftoken);
	},
      type: "GET",
      url: url,
      dataType: "json",
      success: function(data, textStatus, jqXHR, response_url){
    	  				callback.call(null, data);
                        },
      error: function(jqXHR, textStatus, errorThrown){
                        	alert("error");	
                        	$.each(jqXHR, function(k, item){
                        		if(k == "responseText"){
                        		alert(k + " " +item);
                        		}
                        	});
                        }
             });
}


function postJSON(method, url, data, callback){
$.ajax({
	 beforeSend: function(xhrObj){
	xhrObj.setRequestHeader("Content-Type","application/json");
	xhrObj.setRequestHeader("Accept","application/json");
	xhrObj.setRequestHeader("X-CSRFToken", csrftoken);
	},
      type: method,
      url: url,
      dataType: "json",
      data:
      JSON.stringify(data),
      success: function(data, textStatus, jqXHR, response_url){
    	  				var response_url = '';
    	  				response_url = String(data.url);
    	  				callback.call(null, response_url);
                        },
      error: function(jqXHR, textStatus, errorThrown){
                        	alert("error");	
                        	$.each(jqXHR, function(k, item){
                        		if(k == "responseText"){
                        		alert(k + " " +item);
                        		}
                        	});
                        }
             });
}

function getFormData($form){
    var unindexed_array = $form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}


$('#order_button').click(function(){ 	

	var resturant_id = $('#order_restaurant').text();
	
	postJSON("POST", "/order/", {"restaurant": "/restaurant/" + resturant_id + "/"} , function (order_url) {

		$('.orderitem').each(function(i, obj) {
			postJSON("POST", "/order-item/", {"order": order_url, "menu_item": "/menu-item/"+ $(this).attr("rest_id") +"/"} , function (url) {
			});
		});
		postJSON("POST","/address/", getFormData($('#address_form')) , function (address_url) {
			postJSON("PATCH", order_url, {"address": address_url, "status" : "1"} , function (test) {
				submitOrder();
				//start polling for restaurant response
				var i = 1;
				var refreshIntervalId = setInterval(function(){
					getJSON( order_url ,
				        function(data){ 
				        	if (data.status == "1"){
				        		$('.status').text("Waiting for response from restaurant");
				        		//continue polling
				        	}
				        	if (data.status == "2"){
				        		$('.status').text("The restaurant has accepted your order");
				        		clearInterval(refreshIntervalId); //stop polling
				        	}
				        	if (data.status == "3"){
				        		$('.status').text("The restaurant declined your order");
				        		clearInterval(refreshIntervalId); //stop polling
				        	}
				        	if (i == 100){
				        		$('.status').text("The restaurant does not respond");
				        		i = 1;
				        		clearInterval(refreshIntervalId); //stop polling
				        	}
				        });
					}, 3000);
			});
		});
	});
});

function emptyOrder(){
	
}


function updateTotal(){
	var total = 0;
	$('.price').each(function(i, obj) {
		total += parseInt($(this).text());
	});
	$("#total").text("Total: "+ total +"€");
}


$('#order').on('click', '.orderitem', function(){
	$(this).remove();
	updateTotal();
});


var orderitem=0;
$('#menu').on('click', 'button', function(){
	item_id = orderitem++;
	$('<div>', {id: item_id, "class": "orderitem", "rest_id": $(this).attr('id') }).appendTo("#order_item");
	$('<p>', {"class": "name", text: $(this).children("#name").text() }).appendTo("#order_item > div[id='" + item_id +"']");
	$('<p>', {"class": "price", text: $(this).children("#price").text() }).appendTo("#order_item > div[id='" + item_id +"']");
	updateTotal();
});


$('#restaurant').on('click', 'button', function(){
	newOrder();
	//insert empty all
	$('#order > #order_restaurant').text($(this).attr('id'));
	$('#menu').empty();

	var menu_url =  $(this).attr('href') + "menu/";
	getJSON( menu_url ,
	        function(data){
	        	$.each(data, function(i, menu){
	        		$.each(menu, function(j, menu_section){
	        			var menu_id = url2id(menu_section.url)
	        			$('<div>', {id: menu_id, "class": "well"}).appendTo('#menu');
	        			$('<p>', {id: menu_id, href: menu_section.url, text: menu_section.title }).appendTo("div[id='" + menu_id + "']");
	        			getJSON(menu_section.url, function(menu_section_data){
							$.each(menu_section_data, function(k, menu_section_detail){
								if (k == 'menu_item'){
									$.each(menu_section_detail, function(l, menu_item){
										var menu_item_id = url2id(menu_item.url);
										//alert(menu_id + " " + menu_item_id);
										$('<button>', { id: menu_item_id, "class":"btn  btn-warning"}).appendTo("div[id='" + menu_id +"']");
										$.each(menu_item, function(m, menu_item_detail){ //['name', 'price','description','faved']
											if (['name', 'price'].indexOf(m) >= 0) {  
												$('<div>', {id: m, text: menu_item_detail}).appendTo("div[id='" + menu_id +"'] > button[id='" + menu_item_id +"']");
							        		}
										});
									});
								}
							});
						});
	        	  });
	          });
});
	
	
	

});
	

function myFunction()
{
alert("I am an aflert box!");
}

function url2id(url){
	if(url.slice(-1) == "/") {
		url = url.slice(0, -1);
	}
	url = url.slice(url.lastIndexOf('/') + 1);
	return url
}

/*
function geome(url){
	var geocoder = new google.maps.Geocoder();
	var lat = position.coords.latitude;
	var lng = position.coords.longitude;
	var latlng = new google.maps.LatLng(lat, lng);
	geocoder.geocode({'latLng': latlng}, function(results, status) {
	    if (status == google.maps.GeocoderStatus.OK) {
	        if (results[1]) {
	            $('#address').text(results[0].formatted_address).show();
	        }
	    } else {
	         alert("Geocoder failed due to: " + status);
	    }
	});
}
*/
	
var geocoder;
  var map;
  function initialize() {
    geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(-34.397, 150.644);
  }

  
  function codeAddress(callback) {
    var address = $("#search_box").val();
    geocoder.geocode( { 'address': address}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
    	  callback( { latitude: results[0].geometry.location.lat(), longitude: results[0].geometry.location.lng() });
      } else {
        alert("Geocode was not successful for the following reason: " + status);
      }
    });
}

///////////////////
//new functions
////////////////////

function newSearch(){
	$('#search_window').hide();
	$('#restaurant').empty()
	
	$('#order_window').show();
	$('#address_window').show();
	$('#order_info_window').show();
	
	$('#menu').empty();
	$('#order > #order_restaurant').empty();
	$('#order > #order_item').empty();
	$('#order > #total').empty();
}


function newOrder(){
	$('#menu').empty();
	$('#order > #order_restaurant').empty();
	$('#order > #order_item').empty();
	$('#order > #total').empty();
}

function submitOrder(){
	$('#notification_window').show();
	$('#order_button').hide();
	$('#address_window').hide();
	$('#restaurant').empty();
	$('#order_window').hide();
	$('#menu').empty();
}

////////////////////
////////////////////
////////////////////

$('#restaurant_button').click(function(){
	newSearch();
	
	initialize();
	codeAddress( function(location){
		//29 Eustace St, Rathmines, Dublin
		//alert("/restaurant/?latitude=" + location.latitude +"&longitude="+location.longitude);
		getJSON( String("/restaurant/?latitude=" + location.latitude +"&longitude="+location.longitude), function(data){
	        $.each(data, function(i,restaurant){
	      	  restaurant_id = url2id(restaurant.url);
	      	  $('<button>', {id: restaurant_id, href: restaurant.url, "class":"btn  btn-info"}).appendTo('#restaurant');
	      	  $.each(restaurant, function(j,restaurant_detail){
	      		  if( $.inArray( j, ["name", "rating"]) >= 0){
	      			  $('<div>', {id: j, text: restaurant_detail}).appendTo("div[id='restaurant'] > button[id='" + restaurant_id +"']");
	      		  }
	      	  });
	        });
	      });
	      
		});
	
	//alert(codeAddress());
	
//alert("erer");
	
	
/*
	
/*
	$.getJSON("/restaurant/",
	        function(data){
	          $.each(data, function(i,restaurant){
	        	  restaurant_id = url2id(restaurant.url);
	        	  $('<button>', {id: restaurant_id, href: restaurant.url}).appendTo('#restaurant');
	        	  $.each(restaurant, function(j,restaurant_detail){
	        		  if( $.inArray( j, ["name", "rating"]) >= 0){
	        			  $('<div>', {id: j, text: restaurant_detail}).appendTo("div[id='restaurant'] > button[id='" + restaurant_id +"']");
	        		  }
	        	  });
	          });
	        });
*/
});

