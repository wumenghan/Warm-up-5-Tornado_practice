// Let user to be either A or B
var player_list = ['A','B'];
//var play = player_list[Math.floor.(Math.random() * player_list.length)];
// Global variable
var g_a_seen = 0;
var g_b_seen = 0;
var g_correct = 0;
jQuery(document).ready(function(){
	$("#message_a").on("keypress",A_player_handler);
	$("#message_a").select();
	$("#message_b").on("keypress",B_player_handler);
	$("#message_a").on("keypress",CompareHandler);
	$("#message_b").on("keypress",CompareHandler);

	poll_A();
	poll_B();
	CompareHandler();
	poll_compare();


});

function A_player_handler(evt){
	
		if(evt.which == 13){
			evt.preventDefault();
		var message_input = document.getElementById("message_a");
		message_input.disabled = true;
		$.ajax({
			url:"/new_a",
			data:{message:message_input.value},
			type:"POST",
			success:function(data){
				message_input.value = "";
				message_input.disabled = false;
				message_input.select();
				}		
			});
		}
}

function poll_A(){
	
		$.ajax({
			url:"/update_a",
			type:"POST",
			data:{num_seen:g_a_seen},
			success:function(data){
			//Display message in browser
			var html_parts = [];
			for (var i = 0; i < data.messages_a.length;i++){
					var text = data.messages_a[i];
					var html = text.replace("&","&amp").replace("<","&lt;").replace(">","&gt;");
					html = '<div class=a_message>'+html+'</div>';
					html_parts.push(html);
					
				}
				document.getElementById("message_a_display").innerHTML = html_parts.join("");

			
				g_a_seen = data.messages_a.length;
				poll_A();
			}
		});
}

function B_player_handler(evt){
	
		if(evt.which == 13){
			evt.preventDefault();
		var message_input = document.getElementById("message_b");
		message_input.disabled = true;
		$.ajax({
			url:"/new_b",
			data:{message:message_input.value},
			type:"POST",
			success:function(data){
				message_input.value = "";
				message_input.disabled = false;
				message_input.select();
				}		
			});
		}
}

function poll_B(){
	
		$.ajax({
			url:"/update_b",
			type:"POST",
			data:{num_seen:g_b_seen},
			success:function(data){
			//Display message in browser
			var html_parts = [];
			for (var i = 0; i < data.messages_b.length;i++){
					var text = data.messages_b[i];
					var html = text.replace("&","&amp").replace("<","&lt;").replace(">","&gt;");
					html = '<div class=b_message>'+html+'</div>';
					html_parts.push(html);
					
				}
				document.getElementById("message_b_display").innerHTML = html_parts.join("");

			
			g_b_seen = data.messages_b.length;
			poll_B();
			}
		});
}

function CompareHandler(){

	$.ajax({
		url:"/compare",
		type:"POST",
		success:alert("compare success")
	
	
	});

}

function poll_compare(){
		
		$.ajax({
			url:"/update_compare",
			type:"POST",
			data:{correct:g_correct},
			success:function(data){
			//print data to brower
			document.getElementById("correct_value").value = data.correct;
			g_correct = data.correct;
			poll_compare();
			}

		
		})


}
