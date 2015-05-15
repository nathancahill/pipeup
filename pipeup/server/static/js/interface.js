
$(function() {
    if (window.location.host !== "pipeup.io") {
        $(".nav .sign-up").hide();

        if (typeof Stream !== 'undefined') {
            Stream.init();
        }
    } else {
        if (typeof StreamPubNub !== 'undefined') {
            StreamPubNub.init();
        }
    }

    function hidePopup(e) {
        if (e) {
            e.preventDefault();
        }

        $('.popup').hide();
        $('.popup-background').hide();
    }

    function showSignupPopup(e) {
        if (e) {
            e.preventDefault();
        }

        $('.popup-signup').show();    
        $('.popup-background').show();    
    }

    function showAboutPopup(e) {
        if (e) {
            e.preventDefault();
        }

        $('.popup-about').show();    
        $('.popup-background').show();    
    }

    function showThanksPopup(e) {
        if (e) {
            e.preventDefault();
        }

        $('.popup-thanks').show();    
        $('.popup-background').show();    
    }

    $(document).bind('keyup', function(e) {
        if (e.which === 27) {
            hidePopup(e);
        }
    });

    $('.sign-up').bind('click', showSignupPopup);
    $('.header .title').bind('click', showAboutPopup);
    $('.popup .close').bind('click', hidePopup);
    $('.popup-background').bind('click', hidePopup);

    $('.popup form').bind('submit', function(e) {
        e.preventDefault();
        $.post("/signup", {email: $("#email").val()});
        hidePopup();
        showThanksPopup(e);
    });

    if (window.location.hash === "#about") {
        showAboutPopup();
    }
});
