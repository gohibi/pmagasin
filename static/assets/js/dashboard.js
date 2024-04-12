$(document).ready(function(){
    $('.list-group-item').click(function(){
        var target = $(this).attr('href');
        $('.content').removeClass('active');
        $(target).addClass('active');
    });
});
