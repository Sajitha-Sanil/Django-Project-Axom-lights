(function($) {
"use strict";

/*------------------------------------------------------------------
[Table of contents]


/*-------------------------------------------
  js wow
--------------------------------------------- */
 new WOW().init();

/*-------------------------------------------
jQuery MeanMenu
--------------------------------------------- */
jQuery(".main-menu").meanmenu();

/*-------------------------------------------
  js scrollup
--------------------------------------------- */
$.scrollUp({
	scrollText: '<i class="fa fa-angle-up"></i>',
	easingType: 'linear',
	scrollSpeed: 900,
	animation: 'fade'
}); 

/*-------------------------------------------
  product slide
--------------------------------------------- */


$(".slide-product.owl-carousel").owlCarousel({
	loop:true,
	autoplay:true,
    autoplaySpeed:2000,
	dots:true,
	nav:false,	  
	items : 1,
	margin:15,
    responsiveClass:true,
    responsive:{
        0:{
            items:1,
            nav:true
        },
        600:{
            items:1,
            nav:false
        },
        1190:{
            items:1,
            nav:false
        },
        1200:{
            items:1,
            nav:true,
            loop:false
        }
    }
});
/*-------------------------------------------
 slide-testimonial
--------------------------------------------- */
const nextIcon='<img src="./assets/images/right-arrow.png" alt="right">';
const prevIcon='<img src="./assets/images/right-arrow.png" alt="prev">';
$(".slide-testimonial.owl-carousel").owlCarousel({
    loop:true,
    autoplay:true,
    autoplaySpeed:2000,
    dots:true,
    nav:true, 
    items : 1,
    margin:15,
    navText: [
        "<i class='fa fa-arrow-left'></i>",
        "<i class='fa fa-arrow-right'></i>"
    ] ,  
    responsive:{
        0:{
            items:1,
            nav:true
        },
        600:{
            items:1,
            nav:true
        },
        1000:{
            items:1,
            nav:true,
            loop:false
        }
    }
});
/*-------------------------------------------
 slide-testimonial
--------------------------------------------- */
$(".slide-parners.owl-carousel").owlCarousel({
    loop:true,
    autoplay:true,
    autoplaySpeed:2000,
    animateOut: 'slideOutDown',
    animateIn: 'flipInX',
    dots:true,
    nav:true,   
    items : 4,
    margin:15,
    navText: [
        "<i class='fa fa-arrow-left'></i>",
        "<i class='fa fa-arrow-right'></i>"
    ] ,  
    responsiveClass:true,
    responsive:{
        0:{
            items:1,
            nav:true
        },
        600:{
            items:2,
            nav:false
        },
        1000:{
            items:4,
            nav:true,
            loop:false
        }
    }
});

/*-------------------------------------------
thumbnail-slider
--------------------------------------------- */

$(document).ready(function () {
    $('#thumbnail-slider').splide({
          fixedWidth : 100,
          fixedHeight : 60,
          gap : 10,
          rewind : true,
          pagination : false,
          cover : true
  });
  });

/*-------------------------------------------
Counter up activation  
--------------------------------------------- */
$('.counter').counterUp({
    delay: 50,
    time: 3000
});

/**
   * Sidebar toggle
   */
if (select('.toggle-sidebar-btn')) {
    on('click', '.toggle-sidebar-btn', function(e) {
      select('body').classList.toggle('toggle-sidebar')
    })
  }

  /**
   * Search bar toggle
   */
  if (select('.search-bar-toggle')) {
    on('click', '.search-bar-toggle', function(e) {
      select('.search-bar').classList.toggle('search-bar-show')
    })
  }



})(jQuery);



