
$(function() {
    Stream.init(key);

    function hidePopup(e) {
        e.preventDefault();

        $('.popup').hide();
        $('.popup-background').hide();
    }

    function showSignupPopup(e) {
        e.preventDefault();

        $('.popup-signup').show();    
        $('.popup-background').show();    
    }

    function showAboutPopup(e) {
        e.preventDefault();

        $('.popup-about').show();    
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
    });
});
