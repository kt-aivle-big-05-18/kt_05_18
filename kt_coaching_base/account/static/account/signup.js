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
