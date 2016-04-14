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

// For user profile
var color = "#000";

function edit() {
    $('button[name=UserProfile]').show(); 
    $('#cancelModify').show();
    $('#modifyProfile').hide();

    $('input[name=username]').show();
    $('input[name=email]').show();
    $('#divUsername').hide();
    $('#divEmail').hide();

    $('input[name=email]').css("background", "white");
}

function cancel() {
    $('button[name=UserProfile]').hide();
    $('#cancelModify').hide(); 
    $('#modifyProfile').show();

    $('input[name=username]').hide();
    //$('input[name=email]').hide();
    $('#divUsername').show();
    $('#divEmail').show();

    $('input[name=email]').css("background", "transparent");
}