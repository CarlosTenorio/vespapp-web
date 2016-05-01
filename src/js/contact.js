// Input Lock
$(document).ready(function(){
  $('textarea').blur(function () {
      $('#sectionContact textarea').each(function () {
          $this = $(this);
          if ( this.value != '' ) {
            $this.addClass('focused');
            $('textarea + label + span').css({'opacity': 1});
          }
          else {
            $this.removeClass('focused');
            $('textarea + label + span').css({'opacity': 0});
          }
      });
  });

  $('#sectionContact .name-box input').blur(function () {
      $('#sectionContact .name-box input').each(function () {
          $this = $(this);
          if ( this.value != '' ) {
            $this.addClass('focused');
            $('.name-box input + label + span').css({'opacity': 1});
          }
          else {
            $this.removeClass('focused');
            $('.name-box input + label + span').css({'opacity': 0});
          }
      });
  });

  $('#sectionContact .email-box input').blur(function () {
      $('#sectionContact .email-box input').each(function () {
          $this = $(this);
          if ( this.value != '' ) {
            $this.addClass('focused');
            $('.email-box input + label + span').css({'opacity': 1});
          }
          else {
            $this.removeClass('focused');
            $('.email-box input + label + span').css({'opacity': 0});
          }
      });
  });

  $('#sectionContact .phone-box input').blur(function () {
      $('#sectionContact .phone-box input').each(function () {
          $this = $(this);
          if ( this.value != '' ) {
            $this.addClass('focused');
            $('.phone-box input + label + span').css({'opacity': 1});
          }
          else {
            $this.removeClass('focused');
            $('.phone-box input + label + span').css({'opacity': 0});
          }
      });
  });
}); 