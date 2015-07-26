(function($){
	if( $('.cd-form-rates').length > 0 ) {
		//set some form parameters
		var device = checkWindowWidth(),
			tableFinalWidth = ( device == 'mobile') ? $(window).width()*0.9 : 210,
			tableFinalHeight = ( device == 'mobile' ) ? 93 : 255;
			formMaxWidth = 900,
			formMaxHeight = 650,
			btnCalculator = $('#submit-calculator')
			formCalculator = $('#form-calculator');
			animating =  false;
			
		//set animation duration/delay
		var	animationDuration = 800,
			delay = 200,
			backAnimationDuration = animationDuration - delay;

		//store DOM elements
		var formPopup = $('.cd-pricing'),
			coverLayer = $('.cd-overlay');


		//select a plan and open the signup form
		formPopup.on('click', 'a', function(event){
			event.preventDefault();
			var rateKey = ($(this).parents('.cd-pricing-footer').parent('li').attr('id'));
			btnCalculator.attr('rateKey',rateKey);
			triggerAnimation( $(this).parents('.cd-pricing-footer').parent('li'), coverLayer, true);
		});

		btnCalculator.on('click',function(event){
			event.preventDefault();

			$.ajax({
				url: '/calculator/rates/'+$(this).attr('rateKey')+'/',
				type: 'POST',
				headers : { "X-CSRFToken": Cookies.get("csrftoken") },
				data: {
					weight: $('#weight').val(),
					width: $('#width').val(),
					height: $('#height').val(),
					depth: $('#depth').val(),
					price: $('#price').val()
				},
				dataType: 'json'
			})
			.done(function(data){
				$('#total').empty();
				$('#total').append(data.response+'Bs');
			})
			.fail(function(jqXHR){
				$('#total').empty();
				$('#total').append(jqXHR.responseJSON.response);
			});
		});

		//close the signup form clicking the 'X' icon, the keyboard 'esc' or the cover layer
		$('.cd-form-rates').on('click', '.cd-close', function(event){
			event.preventDefault();
			triggerAnimation( formPopup.find('.selected-table'), coverLayer, false);
		});
		$(document).keyup(function(event){
			if( event.which=='27' ) {
				triggerAnimation( formPopup.find('.selected-table'), coverLayer, false);
			}
		});
		coverLayer.on('click', function(event){
			event.preventDefault();
			triggerAnimation( formPopup.find('.selected-table'), coverLayer, false);
		});

		//on resize - update form position/size
		$(window).on('resize', function(){
			requestAnimationFrame(updateForm);
		});

	}

	function triggerAnimation(table, layer, bool) {
		if( !animating ) {
			layer.toggleClass('is-visible', bool);
			animateForm(table, bool);
			table.toggleClass('selected-table', bool);
		}
	}

	function animateForm(table, animationType) {
		animating = true;

		var tableWidth = table.width(),
			tableHeight = table.height(),
			tableTop = table.offset().top - $(window).scrollTop(),
			tableLeft = table.offset().left,
			form = $('.cd-form-rates'),
			formPlan = form.find('.cd-plan-info'),
			formFinalWidth = formWidth(),
			formFinalHeight = formHeight(),
			formTopValue = formTop(formFinalHeight),
			formLeftValue = formLeft(formFinalWidth),
			formTranslateY = tableTop - formTopValue,
			formTranslateX = tableLeft - formLeftValue,
			windowWidth = $(window).width(),
			windowHeight = $(window).height();

		if( animationType ) {//open the form
			//set the proper content for the .cd-plan-info inside the form
			formPlan.html(table.html());

			//animate plan info inside the form - set initial width and hight - then animate them to their final values
			formPlan.velocity(
			{
				'width': tableWidth+'px',
				'height': tableHeight+'px',
			}, 50, function(){
				formPlan.velocity(
				{
					'width': tableFinalWidth+'px',
					'height': tableFinalHeight+'px',
				}, animationDuration, [ 220, 20 ]);
			});

			//animate popout form - set initial width, hight and position - then animate them to their final values
			form.velocity(
			{
				'width': tableWidth+'px',
				'height': tableHeight+'px',
				'top': formTopValue,
				'left': formLeftValue,
				'translateX': formTranslateX+'px',
				'translateY': formTranslateY+'px',
				'opacity': 1,
			}, 50, function(){
				table.addClass('empty-box');
				
				form.velocity(
				{
					'width': formFinalWidth+'px',
					'height': formFinalHeight+'px',
					'translateX': 0,
					'translateY': 0,
				}, animationDuration, [ 220, 20 ], function(){
					animating = false;
					setTimeout(function(){
						form.children('form').addClass('is-scrollable');
					}, 300);
				}).addClass('is-visible');

			});
		} else {//close the form
			form.children('form').removeClass('is-scrollable');

			//animate plan info inside the form to its final dimension
			formPlan.velocity(
			{
				'width': tableWidth+'px',
			}, {
				duration: backAnimationDuration,
				easing: "easeOutCubic",
				delay: delay
			});

			//animate form to its final dimention/position
			form.velocity(
			{
				'width': tableWidth+'px',
				'height': tableHeight+'px',
				'translateX': formTranslateX+'px',
				'translateY': formTranslateY+'px',
			}, {
				duration: backAnimationDuration,
				easing: "easeOutCubic",
				delay: delay,
				complete: function(){
					table.removeClass('empty-box');
					form.velocity({
						'translateX': 0,
						'translateY': 0,
						'opacity' : 0,
					}, 0).find('form').scrollTop(0);
					animating = false;
				}
			}).removeClass('is-visible');

			//target browsers not supporting transitions
			if($('.no-csstransitions').length > 0 ) table.removeClass('empty-box');
			cleanForm();
		}
	}

	function checkWindowWidth() {
		var mq = window.getComputedStyle(document.querySelector('.cd-form-rates'), '::before').getPropertyValue('content').replace(/"/g, '').replace(/'/g, '');
		return mq;
	}

	function cleanForm(){
		$('#weight').val(0);
		$('#width').val(0);
		$('#height').val(0);
		$('#depth').val(0);
		$('#price').val(0);
		$('#total').empty();
		$('#total').append('0Bs.');
	}
	function updateForm() {
		var device = checkWindowWidth(),
			form = $('.cd-form-rates');
		tableFinalWidth = ( device == 'mobile') ? $(window).width()*0.9 : 210;
		tableFinalHeight = ( device == 'mobile' ) ? 93 : 255;
		
		if(form.hasClass('is-visible')) {
			var formFinalWidth = formWidth(),
				formFinalHeight = formHeight(),
				formTopValue = formTop(formFinalHeight),
				formLeftValue = formLeft(formFinalWidth);
			
			form.velocity(
			{
				'width': formFinalWidth,
				'height': formFinalHeight,
				'top': formTopValue,
				'left': formLeftValue,
			}, 0).find('.cd-plan-info').velocity(
			{
				'width': tableFinalWidth+'px',
				'height': tableFinalHeight+'px',
			}, 0);
		}
	}

	//evaluate form dimention/position
	function formWidth() {
		return ( formMaxWidth <= $(window).width()*0.9) ? formMaxWidth : $(window).width()*0.9;
	}
	function formHeight() {
		return ( formMaxHeight <= $(window).height()*0.9) ? formMaxHeight : $(window).height()*0.9;
	}
	function formTop(formHeight) {
		return ($(window).height() - formHeight)/2;
	}
	function formLeft(formWidth) {
		return ($(window).width() - formWidth)/2;
	}

})(jQuery);