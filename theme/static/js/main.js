/**
 * Created by adubnyak@gmail.com on 01.04.15.
 */

$(document).ready(function(){

    $('#collapse_xs_menu_on').on('click', function(e){
        e.preventDefault();
        $('#collapse_xs_menu').toggle();
        $('.overlay-menu').toggle();

    });

});