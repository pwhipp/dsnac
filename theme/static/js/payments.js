$(document).ready(function(){
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    // Close Checkout on page navigation
    $(window).on('popstate', function() {
        handler.close();
    });


    $('.amount_values').on('change', function(){
        $('#top_amount').text($(this).val());
        $('#id_amount').val($(this).val())
    });
    $('#id_memory_of').on('change', function(){
        $('#memory_types').toggle();
    });
    // Todo
    $('#id_anonymous').on('change', function(){
        var anon = $('#id_full_name_notification');
        if (anon.prop('checked', true)) {
            anon.prop('readonly', true);
        } else {
            anon.prop('readonly', false);
        }

    });
    $('.donate_now').on('click', function(){
        $(this).hide();
    });

    $('.close').on('click', function(){
        window.location.href = "/";
    });

    $('#reset_fields').on('click', function(){
        $('#donation_form').trigger("reset");
    });

    var getUrlParameter = function getUrlParameter(sParam) {
        var sPageURL = decodeURIComponent(window.location.search.substring(1)),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;

        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');

            if (sParameterName[0] === sParam) {
                return sParameterName[1] === undefined ? true : sParameterName[1];
            }
        }
    };

    $(document).ready(function () {
        var result = getUrlParameter('success');
        if(result){
            $('#thanks_message').modal('show');
        }
    });

});