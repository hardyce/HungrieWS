<html>
<head>
<title>jQuery Hello World</title>
 
<script type="text/javascript" src="/home/jquery-1.9.1.min.js"></script>
 
</head>
 
<body>
 

<button id="ajax">ajax call</button>
<button id="json">json</button>

<input type="button" onclick="myFunction()" value="Show alert box">


<script type="text/javascript">

$(document).ready(function(){
 $("#msgid").html("This is Hello World by JQuery");
});

function myFunction()
{
alert("I am an alert box!");
}
/*
//var rootURL = ;
	
    $('#json').click(function(){ 
        alert('json');
         $.getJSON('/restaurant/',
         function(data) {
            alert(data);         
          });   
    });

    $('#ajax').click(function(){ 
    alert("I am an alert box!");
    
        alert('ajax');
         $.ajax({ 
             type: "GET",
             dataType: "json",
             url: '/restaurant/',
             success: function(data){ alert(data); } 
         });
         
    });
*/

</script>
 
This is Hello World by HTML
 
<div id="msgid">
</div>

<div id="restaurants">
</div>
 
</body>
</html>