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

function successProfile(msg){
  swal({
      title: "Yuju!",
      text: msg,
      type: "success",
      timer: 4000,
      animation: "pop",
      confirmButtonText: "Vale"
  });
}

function successUserActions(msg){
  swal({
      title: "¡Te echaremos de menos!",
      text: msg,
      type: "success",
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
    confirmButtonColor: "#55dd57",
    confirmButtonText: "¡Registrarme! o Login",
    closeOnConfirm: false,
    closeOnCancel: false
  },
  function(isConfirm){
    if (isConfirm) {
      window.location = '/login/';
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