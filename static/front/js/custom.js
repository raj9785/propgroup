(function ($) {

    let leftSide = $('.pxp-content-side.pxp-content-left');
    let rightSide = $('.pxp-map-side.pxp-map-right');

    $('.left-arrow').on('click', () => {
        // alert('leftArrow clicked');
        if (leftSide.hasClass('w-80p')) {
            $(leftSide).removeClass('w-80p');
            $(rightSide).removeClass('w-20p');
        } else {
            $(leftSide).addClass('w-20p');
            $(rightSide).addClass('w-80p');
            $(this).css('opacity', 0)
        }
    });
    $('.right-arrow').on('click', () => {
        // alert('rightArrow clicked');
        if (rightSide.hasClass('w-80p')) {

            $(leftSide).removeClass('w-20p');
            $(rightSide).removeClass('w-80p');
        } else {

            $(leftSide).addClass('w-80p');
            $(rightSide).addClass('w-20p');
            $(this).css('opacity', 0)
        }
    });
    $(rightSide).on('dblclick', () => {
        if (rightSide.hasClass('w-100p')) {
            $(leftSide).removeClass('w-0p');
            $(rightSide).removeClass('w-100p');
        } else {
            $(leftSide).addClass('w-0p');
            $(rightSide).addClass('w-100p');
        }
    });

    $("#thumbSlider .thumb").on("click", function(){
        $(this).addClass("active");
        $(this).siblings().removeClass("active");
    
    });

})(jQuery);