// $('.questionRadio').click(function(){
//    if ($(this).hasClass('active')) {
//    	//do nothing
//    }else{
//    	$('.questionRadio label').addClass('active');
//    	//$(this).addClass('active');
//    }
// });


$(document).ready(function(){
    $(".questionRadio").click(function(){
        $(".questionRadio").removeClass("active");
        $(this).addClass('active');
    });
});

