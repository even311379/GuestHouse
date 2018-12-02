; (function ($) {
    "use strict"


    var nav_offset_top = $('header').height() - 50;
    /*-------------------------------------------------------------------------------
	  Navbar 
	-------------------------------------------------------------------------------*/

    //* Navbar Fixed  
    function navbarFixed() {
        if ($('.header_area').length) {
            $(window).scroll(function () {
                var scroll = $(window).scrollTop();
                if (scroll >= nav_offset_top) {
                    $(".header_area").addClass("navbar_fixed");
                } else {
                    $(".header_area").removeClass("navbar_fixed");
                }
            });
        };
    };
    navbarFixed();


    /*----------------------------------------------------*/
    /*  Parallax Effect js
    /*----------------------------------------------------*/
    function parallaxEffect() {
        $('.bg-parallax').parallax();
    }
    parallaxEffect();


    //	$('.courses_area').imagesLoaded(function(){
    //        $('.courses_inner').isotope({ 
    //            layoutMode: 'masonry',
    //			percentPosition: true,
    //			masonry: {
    //				columnWidth: 1,
    //			}
    //        })
    //    });




    /*----------------------------------------------------*/
    /*  portfolio_isotope
    /*----------------------------------------------------*/

    //	$('.courses_inner').imagesLoaded(function(){
    //        $('.courses_inner').isotope({ 
    //            layoutMode: 'masonry',
    //            percentPosition:true,
    //            masonry: {
    //                columnWidth: 1,
    //            }            
    //        })
    //    });


    /*----------------------------------------------------*/
    /*  Clients Slider
    /*----------------------------------------------------*/
    //    function clients_slider(){
    //        if ( $('.clients_slider').length ){
    //            $('.clients_slider').owlCarousel({
    //                loop:true,
    //                margin: 30,
    //                items: 5,
    //                nav: false,
    //                autoplay: false,
    //                smartSpeed: 1500,
    //                dots:false, 
    //                responsiveClass: true,
    //                responsive: {
    //                    0: {
    //                        items: 1,
    //                    },
    //                    400: {
    //                        items: 2,
    //                    },
    //                    575: {
    //                        items: 3,
    //                    },
    //                    768: {
    //                        items: 4,
    //                    },
    //                    992: {
    //                        items: 5,
    //                    }
    //                }
    //            })
    //        }
    //    }
    //    clients_slider();
    /*----------------------------------------------------*/
    /*  MailChimp Slider
    /*----------------------------------------------------*/
    function mailChimp() {
        $('#mc_embed_signup').find('form').ajaxChimp();
    }
    mailChimp();

    $('select').niceSelect();

    /*----------------------------------------------------*/
    /*  Simple LightBox js
    /*----------------------------------------------------*/
    $('.imageGallery1 .light').simpleLightbox();

    $('.counter').counterUp({
        delay: 10,
        time: 1000
    });

    /*----------------------------------------------------*/
    /*  Testimonials Slider
    /*----------------------------------------------------*/
    function testimonials_slider() {
        if ($('.testi-slider').length) {
            $('.testi-slider').owlCarousel({
                loop: true,
                margin: 30,
                items: 1,
                nav: false,
                autoplay: false,
                smartSpeed: 1500,
                dots: true,
                //				navContainer: '.testimonials_area',
                //                navText: ['<i class="lnr lnr-arrow-up"></i>','<i class="lnr lnr-arrow-down"></i>'],
                responsiveClass: true,
                thumbs: true,
                thumbsPrerendered: true
            })
        }
    }
    testimonials_slider();

    function room_slider() {
        if ($('.owl-room').length) {
            $('.owl-room').owlCarousel({
                items: 1,
                loop: true,
                margin: 0,
                dots: false,
                autoplay: true,
                nav: true,
                navText: ["<span class='lnr lnr-arrow-up'></span>", "<span class='lnr lnr-arrow-down'></span>"]
            });
        }
    }

    room_slider();

    $(document).ready(function () {
        $('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({
            disableOn: 700,
            type: 'iframe',
            mainClass: 'mfp-fade',
            removalDelay: 160,
            preloader: false,

            fixedContentPos: false
        });

        $('.play-btn').magnificPopup({
            type: 'iframe',
            mainClass: 'mfp-fade',
            removalDelay: 160,
            preloader: false,
            fixedContentPos: false
        });
    });


    // Booking Area
    $("#CheckIn").datepicker();
    $("#CheckOut").datepicker();
    $('.lnr .lnr-arrow-down').on("click", function () {
        $("#CheckIn").focus();
    });
    $('.lnr .lnr-arrow-down').on("click", function () {
        $("#CheckOut").focus();
    });

    /* -------------------------------------------------------------------
    /* Isotop Js
    /*------------------------------------------------------------------ */
    $(window).load(function () {
        $('.gallery-filter ul li').click(function () {
            var data = $(this).attr('data-filter');
            $workGrid.isotope({
                filter: data
            })
        });

        if (document.getElementById("gallery")) {
            var $workGrid = $(".gallery-grid").isotope({
                itemSelector: ".all",
                percentPosition: true,
                masonry: {
                    columnWidth: ".all"
                }
            })
        };
    });

    /* -------------------------------------------------------------------
    /* Magnific Popup Js
    /*------------------------------------------------------------------ */
    $('.img-pop-home').magnificPopup({
        type: 'image',
        gallery: {
            enabled: true
        }
    });

    /*----------------------------------------------------*/
    /*  Google map js
    /*----------------------------------------------------*/

    if (document.getElementById("mapBox")) {
        google.maps.event.addDomListener(window, 'load', init);

        function init() {
            var mapOptions = {
                zoom: 11,
                center: new google.maps.LatLng(39.305, -76.617), // New York
                styles: [{
                    "featureType": "water",
                    "elementType": "geometry",
                    "stylers": [{
                        "color": "#e9e9e9"
                    }, {
                        "lightness": 17
                    }]
                }, {
                    "featureType": "landscape",
                    "elementType": "geometry",
                    "stylers": [{
                        "color": "#f5f5f5"
                    }, {
                        "lightness": 20
                    }]
                }, {
                    "featureType": "road.highway",
                    "elementType": "geometry.fill",
                    "stylers": [{
                        "color": "#ffffff"
                    }, {
                        "lightness": 17
                    }]
                }, {
                    "featureType": "road.highway",
                    "elementType": "geometry.stroke",
                    "stylers": [{
                        "color": "#ffffff"
                    }, {
                        "lightness": 29
                    }, {
                        "weight": 0.2
                    }]
                }, {
                    "featureType": "road.arterial",
                    "elementType": "geometry",
                    "stylers": [{
                        "color": "#ffffff"
                    }, {
                        "lightness": 18
                    }]
                }, {
                    "featureType": "road.local",
                    "elementType": "geometry",
                    "stylers": [{
                        "color": "#ffffff"
                    }, {
                        "lightness": 16
                    }]
                }, {
                    "featureType": "poi",
                    "elementType": "geometry",
                    "stylers": [{
                        "color": "#f5f5f5"
                    }, {
                        "lightness": 21
                    }]
                }, {
                    "featureType": "poi.park",
                    "elementType": "geometry",
                    "stylers": [{
                        "color": "#dedede"
                    }, {
                        "lightness": 21
                    }]
                }, {
                    "elementType": "labels.text.stroke",
                    "stylers": [{
                        "visibility": "on"
                    }, {
                        "color": "#ffffff"
                    }, {
                        "lightness": 16
                    }]
                }, {
                    "elementType": "labels.text.fill",
                    "stylers": [{
                        "saturation": 36
                    }, {
                        "color": "#333333"
                    }, {
                        "lightness": 40
                    }]
                }, {
                    "elementType": "labels.icon",
                    "stylers": [{
                        "visibility": "off"
                    }]
                }, {
                    "featureType": "transit",
                    "elementType": "geometry",
                    "stylers": [{
                        "color": "#f2f2f2"
                    }, {
                        "lightness": 19
                    }]
                }, {
                    "featureType": "administrative",
                    "elementType": "geometry.fill",
                    "stylers": [{
                        "color": "#fefefe"
                    }, {
                        "lightness": 20
                    }]
                }, {
                    "featureType": "administrative",
                    "elementType": "geometry.stroke",
                    "stylers": [{
                        "color": "#fefefe"
                    }, {
                        "lightness": 17
                    }, {
                        "weight": 1.2
                    }]
                }]
            };
            var mapElement = document.getElementById('mapBox');
            var map = new google.maps.Map(mapElement, mapOptions);
            var marker = new google.maps.Marker({
                position: new google.maps.LatLng(39.305, -76.617),
                map: map,
                title: 'Snazzy!'
            });
        }
    }


})(jQuery)