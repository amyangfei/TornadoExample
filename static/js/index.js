$(document).ready(function randurl(){
	$.getJSON('/article/random', function(res){
		document.getElementById('next').href = '/article/' + res.short_url;
	})
});

$(document).keydown(function(event){
    if(event.keyCode == 37){
       to_left(); 
    }else if (event.keyCode == 39){ 
       to_right(); 
    } 
});

function to_left(){
	alert('left');
}

function to_right(){
	short_url = $('#next').attr('href')
//	alert(short_url);
	window.location.href = short_url;
}