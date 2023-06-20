// 모달 띄우기 코드
$(document).ready(function() {
    $("#add_feed").on("click", function() {
      const modal = $("#modal_add_feed");
      modal.css("display", "flex");
    //   $(".modal_overlay").show();
    //   $("body").css("overflow-y", "hidden"); // 스크롤 없애기
    
        console.log(window.pageYOffset + " 위치"); // 로그 찍기
    });

// 모달 닫기 코드
    $("#close_modal").on("click", function() {
        const modal = $("#modal_add_feed");
        modal.css("display", "none");
        $("body").css("overflow-y", "visible");
    });
  });