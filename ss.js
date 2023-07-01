$(document).ready(function () {

    var chatContainer = $("#chat-container");




    $("#send-btn").click(function () {

        sendMessage();

    });




    $("#user-input").keypress(function (event) {

        if (event.which === 13) {

            event.preventDefault();

            sendMessage();

        }

    });




    $("#end_btn").click(function () {

        window.location.href = "/rpg/loading/";

    });




    function sendMessage() {

        var userInput = $("#user-input").val();
        if (userInput !== "") {
            let userImageSrc = document.getElementById("myp_info_image").src;
            chatContainer.append("<div class='user_message'>"
                + userInput
                + "<img class='user_profile' src='" + userImageSrc + "' alt='사용자이미지'>"
                + "</div>");
            scrollToBottom();
            print(userImageSrc)

            $.ajax({

                url: "/rpg/rpg_start/",

                type: "POST",

                data: {

                    message: userInput

                },

                success: function (response) {

                    var audioID = "myAudio" + Date.now();  // 고유한 id를 생성합니다.



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

                        volumeIcons[i].onclick = function () {

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



                error: function (xhr, errmsg, err) {

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