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

function successUp(msg){   
  swal({
    title: "¡Gracias por enviar tu avispamiento!",
    text: msg,
    type: "success",
    showCancelButton: true,
    cancelButtonText: "No, gracias",
    confirmButtonColor: "#DD6B55",
    confirmButtonText: "¡Registrarme!",
    closeOnConfirm: false,
    closeOnCancel: false
  },
  function(isConfirm){
    if (isConfirm) {
      window.location = '/signup/';
    }else {  
      swal({
        title: "Puedes registrarte en cuelaquier otro momento",
        text: "Muchas gracias por tu colaboración ;)",
        type: "info",
        confirmButtonText: "OK",
      },
      function(isConfirm){
        if (isConfirm) {
          window.location = '/';
        }
      });
    }    
  });
}


swal({
  title: "Are you sure?",
  text: "You will not be able to recover this imaginary file!",
  type: "warning",
  showCancelButton: true,
  confirmButtonColor: "#DD6B55",
  confirmButtonText: "Yes, delete it!",
  cancelButtonText: "No, cancel plx!",
  closeOnConfirm: false,
  closeOnCancel: false
},
function(isConfirm){
  if (isConfirm) {
    swal("Deleted!", "Your imaginary file has been deleted.", "success");
  } else {
      swal("Cancelled", "Your imaginary file is safe :)", "error");
  }
});