$(document).ready(function () {
    // 로그인 확인 함수
    function loggedIn(userIsAuthenticated) {
        return userIsAuthenticated.toLowerCase() === "true";
    }

    // 각 box 클릭 이벤트 수정
    $(".myp_click").click(function (event) {
        const userIsAuthenticated = $("#user-data").attr("data-user-is-authenticated");
    
        if (!loggedIn(userIsAuthenticated)) {
            alert("로그인이 필요합니다.");
            event.preventDefault();
            event.stopPropagation();
        }
    });    
});
