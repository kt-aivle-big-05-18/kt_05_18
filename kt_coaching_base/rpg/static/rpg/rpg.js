// 사이드바
/* EXPANDER MENU */
const showMenu = (toggleId, navbarId, bodyId) => {
    const toggle = document.getElementById(toggleId),
    navbar = document.getElementById(navbarId),
    bodypadding = document.getElementById(bodyId)

    if( toggle && navbar ) {
        toggle.addEventListener('click', ()=>{
            navbar.classList.toggle('expander');

            bodypadding.classList.toggle('body-pd')
        })
    }
}

// grow 예시 질문 팝업창
  

showMenu('nav-toggle', 'navbar', 'body-pd')

/* LINK ACTIVE */
const linkColor = document.querySelectorAll('.nav__link')
function colorLink() {
    linkColor.forEach(l=> l.classList.remove('active'))
    this.classList.add('active')
}
linkColor.forEach(l=> l.addEventListener('click', colorLink))

/* COLLAPSE MENU */
const linkCollapse = document.getElementsByClassName('collapse__link')
var i

for(i=0;i<linkCollapse.length;i++) {
    linkCollapse[i].addEventListener('click', function(){
        const collapseMenu = this.nextElementSibling
        collapseMenu.classList.toggle('showCollapse')

        const rotate = collapseMenu.previousElementSibling
        rotate.classList.toggle('rotate')
    });
}

// =====================================================================
// 시뮬레이션 메인
$(document).ready(function() {
    var chatContainer = $("#chat-container");

    $("#send-btn").click(function() {
        sendMessage();
    });

    $("#user-input").keypress(function(event) {
        if (event.which === 13) {
            sendMessage();
        }
    });

    $("#end_btn").click(function() {
        window.location.href = "/rpg/loading/";
    });

    function sendMessage() {
        var userInput = $("#user-input").val();
        if (userInput !== "") {
            chatContainer.append("<div class='user_message'>" 
            + userInput
            + "<img class='user_profile' src='/static/img/won.png' alt='사용자이미지'>"
            + "</div>");
            scrollToBottom();

            $.ajax({
                url: "/rpg/rpg_start/",
                type: "POST",
                data: {
                    message: userInput
                },
                success: function(response) {
                    var audioID = "myAudio" + Date.now();  // 고유한 id를 생성합니다.
                    document.getElementById('grow_count').innerHTML = response.grow;
                    chatContainer.append("<div class = 'grow_info'>" + response.grow_info + "</div>")
                    chatContainer.append("<div class='assistant_message'>"
                    + "<div class='assistant_message_left'>"
                    + "<img class='assistant_profile' src='/static/img/young_male.png' alt='페르소나이미지'>"
                    + response.message
                    + "</div>"
                    + "<ion-icon class='assistant_message_icon' name='volume-medium-outline' data-audio-id='" + audioID + "'></ion-icon>"
                    + "</div>");
                    document.getElementById('score').innerHTML = response.score + '점';
                
                    var audioElement = document.createElement("audio");
                    audioElement.src = "data:audio/wav;base64," + response.voice;
                    audioElement.id = audioID;
                
                    var volumeIcons = document.getElementsByClassName('assistant_message_icon');
                    for (var i = 0; i < volumeIcons.length; i++) {
                        volumeIcons[i].onclick = function() {
                            var audioID = this.getAttribute('data-audio-id');
                            var audioToPlay = document.getElementById(audioID);
                
                            if (audioToPlay.paused) {
                                audioToPlay.play();
                                this.name = 'volume-high-outline';
                            } else {
                                audioToPlay.pause();
                                audioToPlay.currentTime = 0;
                                this.name = 'volume-medium-outline';
                            }
                        };
                    }
                
                    chatContainer.append(audioElement);
                    scrollToBottom();
                },
                
                error: function(xhr, errmsg, err) {
                    console.log(errmsg);
                    chatContainer.append(errmsg);
                }
            });

            $("#user-input").val("");
        }
    }

    function scrollToBottom() {
        chatContainer.scrollTop(chatContainer[0].scrollHeight);
    }

//--------------------------------stt--------------------------------------//
    const record = document.getElementById('record');
    let isRecording = false;
    let isPlaying = false;
    let audio = null;

    if (navigator.mediaDevices) {
        var constraints = {
            audio: true
        };
    
        let chunks = [];
    
        navigator.mediaDevices.getUserMedia(constraints)
        .then(stream => {
            const mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });  // mimeType을 audio/webm으로 설정
    
            record.onclick = () => {
                if (!isRecording) {
                    mediaRecorder.start();
                    isRecording = true;
                    // record.style.background = "#BDF2F6";
                    record.style.color = "#B21818";
                } else {
                    mediaRecorder.stop();
                    isRecording = false;
                    record.style.background = "";
                    record.style.color = "";
                }
            };
    
            mediaRecorder.onstop = e => {
                audio = document.createElement('audio');
                audio.setAttribute('controls', '');
    
                const blob = new Blob(chunks, { type: 'audio/webm' });  // blob type을 audio/webm으로 설정
    
                chunks = [];
    
                const audioURL = URL.createObjectURL(blob);
                audio.src = audioURL;
                
                let formData = new FormData();
                formData.append('audio_data', blob);
    
                $.ajax({
                    url: "/rpg/stt/",
                    type: "POST",
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function(response) {
                        $("#user-input").val(response.text);
                    },
                    error: function(xhr, errmsg, err) {
                        console.log(errmsg);
                    }
                });
            };
    
            mediaRecorder.ondataavailable = e => {
                chunks.push(e.data);
            };
        })
        .catch(err => {
            console.log("오류 발생 : " + err)
        });
    }
    

    const soundClips = document.getElementById('sound-clips');
    soundClips.addEventListener('click', function() {
        if(audio) {
            if (!isPlaying) {
                audio.play();
                isPlaying = true;
                soundClips.textContent = '정지';
            } else {
                audio.pause();
                audio.currentTime = 0;
                isPlaying = false;
                soundClips.textContent = '재생';
            }
        }
    });
    
    // 오디오의 재생이 끝나면 '재생'으로 버튼 텍스트 변경
    audio.addEventListener('ended', function() {
        isPlaying = false;
        soundClips.textContent = '재생';
    });
});

// 모달창 //
document.addEventListener("DOMContentLoaded", function() {
    // 토글 버튼 클릭 이벤트
    document.getElementById("grow-ex").addEventListener("click", function() {
      showModal();
    });
  
    // 모달 표시 함수
    function showModal() {
      var modalContent = document.getElementById("modalContent");
      var modalImage = document.getElementById("modalImage");
      modalImage.src = "/static/img/grow_ex.png";
      modalImage.alt = "Grow Example";
  
      document.getElementById("modalWrap").style.display = "block";
    }
  
    // 모달 숨기는 함수
    function hideModal() {
      document.getElementById("modalWrap").style.display = "none";
    }
  
    // 모달 닫기 버튼 클릭 이벤트
    document.getElementById("closeBtn").addEventListener("click", hideModal);
  
    // 모달 영역 외부 클릭 이벤트
    document.getElementById("modalWrap").addEventListener("click", function(e) {
      if (e.target.id === "modalWrap") {
        hideModal();
      }
    });
  });