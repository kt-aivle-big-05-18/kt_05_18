// 아이디 저장 함수
function saveId() {
  var userId = document.getElementById('userid').value; // 아이디 입력 필드의 값 가져오기
  if (userId) {
    document.cookie = "savedId=" + userId + "; expires=Fri, 31 Dec 9999 23:59:59 GMT"; // 쿠키에 아이디 저장
  } else {
    // 아이디 입력 필드가 비어있는 경우 쿠키에서 아이디 제거
    document.cookie = "savedId=; expires=Thu, 01 Jan 1970 00:00:00 GMT";
  }
}

// 페이지 로드 시 저장된 아이디가 있는지 확인하여 아이디 필드에 자동 작성
window.addEventListener('load', function() {
  var savedId = getCookie("savedId");
  if (savedId !== "") {
    document.getElementById('userid').value = savedId;
    document.getElementById('id-save-checkbox').checked = true;
  }
});

// 쿠키 가져오기
function getCookie(cookieName) {
  var name = cookieName + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var cookieArray = decodedCookie.split(';');
  for (var i = 0; i < cookieArray.length; i++) {
    var cookie = cookieArray[i];
    while (cookie.charAt(0) === ' ') {
      cookie = cookie.substring(1);
    }
    if (cookie.indexOf(name) === 0) {
      return cookie.substring(name.length, cookie.length);
    }
  }
  return "";
}
