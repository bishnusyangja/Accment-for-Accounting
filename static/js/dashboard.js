$(document).ready(function () {
		$('.date-picker').datepicker({autoclose: true});

    $('#day-journal-selection-button').on('click', function () {
        window.location = '/day/' + $('#day-journal-date').val();
    });

		$(function(){
		  $('.flip-container').mouseenter(function(){
		      $(this).find('.flip-body').addClass('open');
		  });
		  $('.flip-container').mouseleave(function(){
		      if(!$('.datepicker').is(":visible")){
		          $(this).find('.flip-body').removeClass('open');
		      }
		  });
		});

});


