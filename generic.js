$(document).ready(function() {

//   /* resize fonts for small/mobile screen */
//   $('body').flowtype({
//    minimum   : 500,
//    maximum   : 600,
//    minFont   : 12,
//    maxFont   : 30,
//    fontRatio : 30
//   });
//

$("#fittext0").fitText();
$("#fittext1").fitText(1.7,{ minFontSize: '22px', maxFontSize: '28px' });
$("#fittext2").fitText(1.7, { minFontSize: '31px', maxFontSize: '42px' });
 });

// every time you resize the window set equale height for all cards in homepage
$(window).resize(function() {
 var heig = $(".card-inner").first().height(); // first card element encountered
 $("div.card-inner:not(:first)").each(function(index) {
  //$(this).height(heig);
  });
});

$(function () {
  /* IP Cores search field */
  $('input#id_search').quicksearch('table tbody tr',{'delay': 300,
    'stripeRows': ['odd', 'even']});
});


$(function() {
  smoothScroll(700);
});

// smoothScroll function is applied from the document ready function
function smoothScroll (duration) {
  //$('a[href^="#"]').on('click', function(event) {
  $('a[href*="#"]').on('click', function(event) { // every link tha has "#" in it

      var target = $( $(this).attr('href') );

      // if link begins with "#" and target exist smoothly go to it
      if( target.length && target.selector.match('^#') ) {
          event.preventDefault();

          // scroll to section
          $('html, body').animate({
              scrollTop: target.offset().top
              //scrollTop: $(window.location.hash).offset().top
          }, duration);
      }
      else{
        event.preventDefault();
        var target = $( $(this).attr('href') );
        console.log(target);
        //window.location = "/"; // go home
        window.location = target.selector.replace('home#','/#');

      }
  });
}

// shop item tabs styling
$(document).ready(function () {
  $('.accordion-tabs').each(function(index) {
    $(this).children('li').first().children('a').addClass('is-active').next().addClass('is-open').show();
  });

  // this correction was necessary to prevent the mulfunciton of links
  // placed inside the tab space.
  //$('.accordion-tabs').on('click', 'li > a', function(event) {
  $('.accordion-tabs').on('click', 'li > a.tab-link', function(event) {
    if (!$(this).hasClass('is-active')) {
      event.preventDefault();
      console.log("bingo");
      var accordionTabs = $(this).closest('.accordion-tabs');
      accordionTabs.find('.is-open').removeClass('is-open').hide();

      $(this).next().toggleClass('is-open').toggle();
      accordionTabs.find('.is-active').removeClass('is-active');
      $(this).addClass('is-active');
    } else {
      event.preventDefault();
    }
  });
});

// code for the modal window
$(function() {
  $("#modal-1").on("change", function() {
    if ($(this).is(":checked")) {
      $("body").addClass("modal-open");
    } else {
      $("body").removeClass("modal-open");
    }
  });
  $(".modal-fade-screen, .modal-close, .soon-close").on("click", function() {
    $(".modal-state:checked").prop("checked", false).change();
  });
  $(".modal-inner").on("click", function(e) {
    e.stopPropagation();
  });
});

// make top page links always visible when you are on a shop page
// this function is optimized for speed
$(document).ready(function() {
  if( $('#PayPalMiniCart').length ){
    var element = $('.links'),
    originalY = element.offset().top;
    element.css('position', 'relative');

    $(window).on('scroll', function(event) {
        var scrollTop = $(window).scrollTop();
        element.hide();
        if (scrollTop<50){
          element.css('top','0px');
          element.show();
          }


        element.stop(false, false).animate({
            top: scrollTop < originalY
                    ? 0
                    : scrollTop - originalY + 5
        }, 3000,function(){element.slideDown(200,"swing");});
    });
  }
});
