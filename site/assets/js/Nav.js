var NavApp = (function () {
    var _private = {
        navbar: "",
        hamburger: "",
        offcanvas: "",
        offoverlay: "",
        firstElement: "",
        body: "",
        search: "",
        iconRightM: "",
        // scrollNavLogo: "",
        init: function (_navbar, _hamburger, _offcanvas, _offoverlay, _body) {
            this.navbar = _navbar;
            this.hamburger = _hamburger;
            this.offcanvas = _offcanvas;
            this.offoverlay = _offoverlay;
            this.body = _body;
            // this.scrollNavLogo = $('#scrollNavLogo');
            this.firstElement = $('header').nextAll('section:eq(0)');
            let searchIcon = $('.searchIcon');
            let navbar = $('#navbar');
            let level1 = $('.level1');
            let level2 = $('.level2');
            let level2wrap = $('.level2_wrap');
            let level3 = $('.level3 a');
            let level3wrap = $('.level3_wrap');
            let returnBtn = $('.return');
            let collpaseBtn = $('.collapseBtn');

            let cart = $('.cart');
            let account = $('.account');

            this.iconRightM = $('.icon_right_m');
            // let searchClose = $('.searchClose');
            let resetIcon = $(".nav-searchbar .reset");
            this.uiBinding();
            searchIcon.on('click', function () {
                document.getElementById("searchbar").style.display = "flex";
                $('.nav-searchbar input[type="text"]').focus();
                if ($(window).width() < 992) {
                    _private.offcanvas.css({ "top": "0", "height": "100vh" });
                }
            });
            // searchClose.on('click', function () {
            //     document.getElementById("searchbar").style.display = "none";
            // });
            resetIcon.on('click', function () {
                document.getElementById("searchbar").style.display = "none";
                if ($(window).width() < 992) {
                    _private.offcanvas.css({ "top": "100%", "height": "calc(100vh - 100%)" });
                }
                // $(this).css("display", "none");
                // $('.nav-searchbar input[type="submit"]').css("display", "none");
                //$('.nav-searchbar input[type="text"]').css("padding-left", "3rem");
                //$(".navbar-collapse form").removeClass("w-100");
                //$(".navbar-nav").css("opacity", "1");
            });
            $('.gotop').on('click', function () {
                $('html,body').animate({ scrollTop: 0 }, 'slow');
                return false;
            });
            const temp = _private.offcanvas.children();


            navbar.on('click', '.level1 > a' , function () {
                if ($(this).parent().find(level2wrap)) {
                    // level1.removeClass("active");
                    if ($(this).parent().hasClass("active")) {
                        ClearAll();
                    } else {
                        level1.removeClass("active");
                        $(this).parent().addClass("active");
                        if ($(window).width() > 992) {
                            let firstLevel2 = $(this).parent().find('.level2_wrap .level2').first();
                            firstLevel2.addClass("active");
                        }
                    }
                    if ($(window).width() < 992) {
                        temp.css("transform", "translateX(-100%)");
                        // level2wrap.css("height", "auto");
                        // _private.offcanvas.css("height", "100vh");
                        // console.log("click level1 < 992")
                    } else {
                        level2wrap.css("height", $(this).parent().find(level3wrap).innerHeight());
                    }
                }
                //_private.offcanvas.addClass('open');
            });
            navbar.on('click', '.level2 > a', function () {
                if ($(this).parent().find(level3wrap)) {
                    $('.level2').removeClass("active");
                    $(this).parent().addClass("active");
                    if ($(window).width() < 992) {
                        temp.css("transform", "translateX(-200%)");
                        // level2wrap.css("height", "auto");
                    } else {
                        level2wrap.css("height", $(this).parent().find(level3wrap).innerHeight());
                    }
                    return false;
                }
            });
            /*navbar.on('click', '.level3', function () {
                let link = $(this).attr("href");
                window.location.href = link;
            });*/
            cart.on('click', function () {
                account.removeClass('active');
                $(this).toggleClass('active');
            });
            account.on('click', function () {
                cart.removeClass('active');
                $(this).toggleClass('active');
            });
            navbar.on('click', '.collapseBtn', function () {
                ClearAll();
                return false;
            });
            navbar.on('click', '.return a', function () {
                console.log("returnBtn clicked");
                if ($(this).parent().siblings().hasClass('level2')) {
                    console.log("returnBtn clicked inside");
                    temp.css("transform", "translateX(0%)");
                    $(this).parent().parent().parent().parent().removeClass("active");


                } else {
                    temp.css("transform", "translateX(-100%)");
                    $(this).parent().parent().parent().parent().parent().parent().removeClass("active");
                }
                return false;
            });
            function ClearAll() {
                $('.level1').removeClass("active");
                $('.level2').removeClass("active");
                cart.removeClass("active");
                account.removeClass("active");
            };
            $(window).resize(function () {
                if ($(window).width() > 992) {
                    temp.css("transform", "");
                    _private.offcanvas.css({ "top": "0", "height": "auto" });
                } else {
                    _private.offcanvas.css({ "top": "100%", "height": "calc(100vh - 100%)" });
                }
            });
        },
        ui: {
            hamburgerClick: function () {
                if (_private.offcanvas.hasClass("open")) {
                    // $('.ham1').css("visibility", "hidden");
                    _private.body.css("overflow", "hidden");
                    _private.offoverlay.addClass("active");
                    _private.iconRightM.css("visibility", "hidden");
                } else {
                    // $('.ham1').css("visibility", "visible");
                    _private.body.css("overflow", "inherit");
                    _private.offoverlay.removeClass("active");
                    _private.iconRightM.css("visibility", "visible");
                }
            },
            // ClearSearch: function () {
            //     $('.search').removeClass('active');
            //     $('.search a').find('form, input').css("width", "34px");
            //     $('.logo').removeClass('active');
            // },
            NavInit: function () {
                let navH = $(".navbar").innerHeight() - 13;
                let base = this;
                $('.select-options').css("top", navH);
                // if ($('.navbar').hasClass('fixed-top')) {
                let second_nav = $('.navbar-nav').not('.right_info');
                let nav_offset_top = second_nav.offset().top;
                _private.firstElement.css('margin-top', "0px");
                $(window).on('load scroll resize', function () {
                    base.Nav3Scroll(nav_offset_top, second_nav);
                });
                // }
                if ($(window).width() < 992) {
                    if ($('.account').length === 0) {
                        $('.search_m').css("right", "1rem");
                    }
                    $('.text_size').css("left", "0");
                    $('.dropdown, .dropdown-menu').addClass('show');
                    $('.dropdown-item.dropdown').removeClass('dropright');
                } else {
                    let $lang_w = $('.lang').outerWidth();
                    $('.text_size').css("left", 'calc(' + $lang_w + 'px + 20px)');
                    $('.dropdown, .dropdown-menu').removeClass('show');
                    $('.dropdown-item.dropdown').addClass('dropright');
                }
            },
            Nav3Scroll: function (_nav_offset_top, _second_nav) {
                if ($(window).width() > 992) {
                    // $('.navbar').removeClass('fixed-top');
                    // if ($(window).scrollTop() > _nav_offset_top) {
                    //     let navColor = $(".navbar").css("background-color");
                    _second_nav.css({ "position": "fixed"});
                    // _private.firstElement.css('margin-top', "96px");
                    if ($(window).scrollTop() > window.innerHeight * 0.5) {
                        _second_nav.css({ "background": "#0f0f0f", "transition": "background 1000ms linear;"});
                    }
                    else if ($(window).scrollTop() < window.innerHeight * 0.9) {
                        _second_nav.css({ "background": "#0f0f0f00"});
                    }
                    //     // _private.scrollNavLogo.css('display', 'block');
                    // } else if ($(window).scrollTop() <= _nav_offset_top) {
                    //     _second_nav.css({ "position": "static", "box-shadow": "none" });
                    //     _private.firstElement.css('margin-top', '0px');
                    //     // _private.scrollNavLogo.css('display', 'none');
                    // }
                } else {
                    $('.navbar').addClass('fixed-top');
                    _second_nav.css({ "border": "none", "position": "static" });
                    // _private.firstElement.css('margin-top', "68px");
                    if ($(window).scrollTop() > window.innerHeight * 0.5) {
                        $('header .navbar').css({ "background-color": "#0f0f0f", "transition": "background 1000ms linear"});
                    }
                    else if ($(window).scrollTop() < window.innerHeight * 0.9) {
                        $('header .navbar').css({ "background-color": "#0f0f0f00"});
                    }
                    if (_private.firstElement.length == 0) {
                        $('#app').css('margin-top', "68px");
                    }
                }
            }
        },
        uiBinding: function () {
            let base = this;
            base.ui.NavInit();

            this.hamburger.on('click', function () {
                _private.offcanvas.toggleClass('open');
                $(this).toggleClass("collapsed");
                base.ui.hamburgerClick();
            });

            // base.body.on('click', function (event) {
            //     if ($(event.target).hasClass('clear')) {
            //         setTimeout(function () {
            //             base.ui.ClearSearch();
            //         }, 100);
            //     } else {
            //         base.ui.ClearSearch();
            //     }
            // });
            base.offoverlay.on('click', function () {
                _private.offcanvas.removeClass("open");
                $(this).removeClass("active");
                _private.body.css("overflow", "inherit");
                // $('.ham1').css("visibility", "visible");
            });

        }
    };
    return {
        init: function (_navbar, _hamburger, _offcanvas, _offoverlay, _body) {
            _private.init(_navbar, _hamburger, _offcanvas, _offoverlay, _body);
        }
    }
}())
$(function () {
    NavApp.init($("#navbar"), $('.navbar-toggler'), $('.offcanvas-collapse'), $('#offcanvas-overlay'), $('body'));

})