// 개인정보 동의 체크 여부 확인
// $(document).ready(function() {
//     // START 버튼 클릭 이벤트
//     $("#startBtn").on("click", function() {
//       const userIsAuthenticated = $( "#user-data" ).attr( "data-user-is-authenticated" );
  
//       if (loggedIn(userIsAuthenticated)) {
//         // 로그인된 상태이면 'rpg:persona' 페이지로 이동
//         // 안 되길래 /rpg/persona -> /rpg로 변경
//         window.location.href = `${window.origin}/rpg/`;
//       } else {
//         // 로그인되지 않은 상태이면 경고 팝업 표시
//         alert("로그인이 필요합니다.");
//       }
//     });
  
//   });

// 개인 정보 처리 방안 팝업
$(function() {
	$("#modal").modal("show");
});

// 모달 띄우기 코드
// $(document).ready(function() {
//     $("#add_feed").on("click", function() {
//       const modal = $("#modal_add_feed");
//       modal.css("display", "flex");
//     //   $(".modal_overlay").show();
//     //   $("body").css("overflow-y", "hidden"); // 스크롤 없애기
    
//         console.log(window.pageYOffset + " 위치"); // 로그 찍기
//     });

// 모달 닫기 코드
//     $("#close_modal").on("click", function() {
//         const modal = $("#modal_add_feed");
//         modal.css("display", "none");
//         $("body").css("overflow-y", "visible");
//     });
//   });
$(document).ready(function() {
    // 중복 체크 여부 변수 초기화
    var isDuplicateChecked = false;
    // 개인정보 처리 체크 여부 변수 초기화
    var isPersonalInfoChecked = false;
  
    // CSRF 토큰 추출
    var csrftoken = getCookie('csrftoken');
  
    $('.signup_duplicate_btn').click(function() {
      var userid = $('#userid').val();
  
      $.ajax({
        url: '/account/check_duplicate/',
        type: 'POST',
        data: {userid: userid},
        dataType: 'json',
        beforeSend: function(xhr, settings) {
          // CSRF 토큰을 요청 헤더에 포함시킴
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(response) {
          if (response.is_taken) {
            $('#duplicate-message').text('* 이미 사용 중인 ID입니다.');
            isDuplicateChecked = false; // 중복된 ID일 경우 체크 여부를 false로 설정
          } else {
            $('#duplicate-message').text('* 사용 가능한 ID입니다.');
            isDuplicateChecked = true; // 사용 가능한 ID일 경우 체크 여부를 true로 설정
          }
        },
        error: function(xhr, errmsg, err) {
          console.log(errmsg);
        }
      });
    });
  
    // 개인정보 처리 체크박스 클릭 이벤트 처리
    $('.signup_content_detail_person_info').click(function() {
      isPersonalInfoChecked = $(this).is(':checked'); // 개인정보 처리 체크 여부를 변수에 저장
    });
  
    // 폼 제출 이벤트를 처리
    $('form').submit(function(event) {
      if (!isDuplicateChecked) {
        event.preventDefault(); // 중복확인을 하지 않은 경우 폼 제출을 막음
        alert('중복확인을 해주세요.');
      } else if (!isPersonalInfoChecked) {
        event.preventDefault(); // 개인정보 처리에 동의하지 않은 경우 폼 제출을 막음
        alert('개인정보 수집 및 이용에 동의해주세요.');
      }
    });
  
    // CSRF 토큰을 쿠키에서 추출하는 함수
    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
});
