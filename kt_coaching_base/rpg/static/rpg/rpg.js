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
            chatContainer.append("<div class='user_message'> " + userInput + "</div>");
            scrollToBottom();

            $.ajax({
                url: "/rpg/rpg_start/",
                type: "POST",
                data: {
                    message: userInput
                },
                success: function(response) {
                    chatContainer.append("<div class='assistant_message'>" + response.message + "</div>");
                    document.getElementById('score').innerHTML = response.score + '점';

                    var audioElement = document.createElement("audio");
                    audioElement.src = "data:audio/wav;base64," + response.voice;
                    audioElement.id = "myAudio";
                    
                    var audioControlButton = document.createElement("button");
                    audioControlButton.innerHTML = "Play Audio";
                    audioControlButton.onclick = function() {
                        if (audioElement.paused) {
                            audioElement.play();
                            this.innerHTML = "Stop Audio";
                        } else {
                            audioElement.pause();
                            audioElement.currentTime = 0;
                            this.innerHTML = "Play Audio";
                        }
                    };
                    
                    chatContainer.append(audioControlButton);
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
                    record.style.background = "#BDF2F6";
                    record.style.color = "black";
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
