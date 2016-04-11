(function(w, $) {
  // Carousel
  jQuery(function($) {
    $('.carousel').carousel({
      interval: 5000,
      keyboard: true
    });
  });



 $("#formSignup").addClass("zoomInDown");
  $("#submit").on('click', function(e){
    e.preventDefault();
    $("#formSignup").addClass("zoomOutUp");
    $('#formSignup').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
      $("body").css('background', '#66be44');
      $(".message").css('opacity', 1);
    });
  });


})(window, jQuery);
