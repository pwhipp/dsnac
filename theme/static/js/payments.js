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


    var handler = StripeCheckout.configure({
        key: 'pk_test_PHJ2QiEjhAH5QZg85GhRZNRx',
        image: '/static/img/theme/snac_logo.png',
        token: function(token) {
            $.ajax({
                url: "/donate/",
                type: "POST",
                data: {
                    stripeToken : token.id,
                    csrfmiddlewaretoken: csrftoken,
                    stripe_amount: $('#amount').val()
                },
                success: function(data) {
                    if (data.success) {
                        console.log('Success');
                        $('#thanks_message').modal('show');
                    }
                },
                dataType: "json"
            });
            // You can access the token ID with `token.id`
        }
    });

    var button_handler = StripeCheckout.configure({
        key: 'pk_test_PHJ2QiEjhAH5QZg85GhRZNRx',
        image: '/static/img/theme/snac_logo.png',
        token: function(token) {
            $.ajax({
                url: "/donate/",
                type: "POST",
                data: {
                    stripeToken : token.id,
                    csrfmiddlewaretoken: csrftoken,
                    stripe_amount: $("input:radio[name='payment']:checked").val()
                },
                success: function(data) {
                    if (data.success) {
                        console.log('Success');
                        $('#thanks_message').modal('show');
                    }
                },
                dataType: "json"
            });
            // You can access the token ID with `token.id`
        }
    });

    $('#donateButton').on('click', function(e) {
        // Open Checkout with further options
        button_handler.open({
            name: 'sikhnationalarchives.com',
            description: '',
            amount: $('#amount').val() + '00'
        });
        e.preventDefault();
    });

    $("input[name='payment']").on('change', function(e) {
        button_handler.open({
            name: 'sikhnationalarchives.com',
            description: '',
            amount: $("input:radio[name='payment']:checked").val() + '00'
        });
        e.preventDefault();
    });


    // Close Checkout on page navigation
    $(window).on('popstate', function() {
        handler.close();
    });

});