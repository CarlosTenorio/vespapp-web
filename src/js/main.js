(function(w, $) {
  // Carousel
  jQuery(function($) {
    $('.carousel').carousel({
      interval: 5000,
      keyboard: true
    });
  });
})(window, jQuery);

function errorForm(msg){
  swal({
      title: "Ups!",
      text: msg,
      type: "error",
      timer: 4000,
      animation: "pop",
      confirmButtonText: "Vale"
  });
}