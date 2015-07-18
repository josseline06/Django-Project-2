var login = "login";
var logout = "logout";
var profile = "profile";
var _history = "history";
var pending_packs = "pending_packs";
var _new = "new";		// Registrar nuevo usuario
var create = "create"; // Crear encomienda
var session = "none"; // variable para manejar las sesiones



function logIn(){
	if(document.getElementById("lemail").value=="" || document.getElementById("lpassword").value==""){
			$("#login").valid({
				rules:{
					lemail:{
						required: true,
					},
					lpassword: {
						required: true
					}

				},
		});
		return;
	}

	console.log("Sended request!");
	$.ajax({
		type: 'GET',		
		dataType: 'jsonp',
		url: "http://atiowl.cloudapp.net/login",
		data: {'email': document.getElementById("lemail").value, 'password': document.getElementById("lpassword").value},
		error: function (jqXHR,textStatus, errorThrown) {
		    console.log(jqXHR);
		    console.log(textStatus);
	            alert("Error: Please see Log");
		},
		success: function (data){
			if(data.length==null){
				console.log("its only one");
				$("#profile").remove();
				$("#profile-contact").hide().append(data['content']).fadeIn('slow');
				session = data['session'];
			}else{				
				console.log(data.content);
			}
		}
	});

}

function getView(resource){
	if(resource != "logout"){
		if(document.getElementById("email").value==="" || document.getElementById("password").value==="" || document.getElementById("repassword").value==="" || document.getElementById("question").value==="" || document.getElementById("answer").value===""){
			$("#register").valid({
				rules:{
						email:{
							required: true
						},
						password: {
							required: true
						},
						repassword:{
							required: true
						},
						question:{
							required: true
						},
						answer:{
							required: true
						}

					}

				});
			return;
		}
	}
	console.log(resource);
	$.ajax({
		type: 'GET',		
		dataType: 'jsonp',
		url: "http://atiowl.cloudapp.net/".concat(resource) ,
		data: {'get':resource,'session': session},
		error: function (jqXHR,textStatus, errorThrown) {
		    console.log(jqXHR);
		    console.log(textStatus);
		    alert("Error: Please see Log");
		},
		success: function (data){
			if(data.length==null){
				console.log("its only one");
				$("#profile").remove();
				$("#profile-contact").hide().append(data['content']).fadeIn('slow');
				if(resource=="logout"){
					session="none";
				}

			}else{				
				console.log(data.content);
			}
		}
	});

}

function getContent(resource){

	if(resource=="profile"){
		console.log(resource);
		$("#tab_paquetes_pendientes").removeClass("active");
		
		$("#tab_historial").removeClass("active");
		
		$("#tab_perfil").addClass("active");

		$("#tab_create").removeClass("active");
		
	}
	if(resource=="history"){
		console.log(resource);
		$("#tab_paquetes_pendientes").removeClass("active");
		
		$("#tab_historial").addClass("active");
		
		$("#tab_perfil").removeClass("active");

		$("#tab_create").removeClass("active");
	}
	if(resource=="pending_packs"){
		console.log(resource);
		$("#tab_paquetes_pendientes").addClass("active");
		
		$("#tab_historial").removeClass("active");
		
		$("#tab_perfil").removeClass("active");

		$("#tab_create").removeClass("active");		
	}

	if(resource=="create"){
		console.log(resource);
		$("#tab_paquetes_pendientes").removeClass("active");
		
		$("#tab_historial").removeClass("active");
		
		$("#tab_perfil").removeClass("active");

		$("#tab_create").addClass("active");
	}

	$.ajax({
		type: 'GET',		
		dataType: 'jsonp',
		url: "http://atiowl.cloudapp.net/".concat(resource) ,
		data: {'get':resource, 'session': session},
		error: function (jqXHR,textStatus, errorThrown) {
		    console.log(jqXHR);
		    console.log(textStatus);
		    alert("Error: Please see Log");
		},
		success: function (data){
			if(data.length==null){
				console.log("its only one");
				$("#content").remove();
				$("#top_menu").hide().append(data['content']).fadeIn('slow');
			}else{				
				console.log(data.content);
			}
		}
	});

}
