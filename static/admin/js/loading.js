function showLoading() {
    // 화면의 높이와 너비
    var maskHeight = $(document).height();
    var maskWidth  = window.document.body.clientWidth;

    // 화면에 출력할 마스크 설정
    var mask = "<div id='mask' style='position:absolute; z-index:1000; background-color:#000000; display:none; left:0; top:0;'></div>";

    //화면에 레이어 추가
    $('body').append(mask)

    $('#mask').css({
        'width':maskWidth,
        'height':maskHeight,
        'opacity':'0.3'
    });

    $("#mask").show();

    $('#loadingStatus').show();
}