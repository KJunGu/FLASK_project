function challenge_choice_on(challenge){
	challenge_name = challenge + "name";
	challenge_message = challenge + "message";

	challenge_name = document.getElementById(challenge_name).innerHTML;
	challenge_message = document.getElementById(challenge_message).innerHTML;


	/*개행, html <, > 사용*/
	challenge_name = challenge_name.replace(/(?:\r\n|\r|\n)/gi, '<br />');
	challenge_name = challenge_name.replace(/&lt;/gi, '<');
	challenge_name = challenge_name.replace(/&gt;/gi, '>');

	challenge_message = challenge_message.replace(/(?:\r\n|\r|\n)/gi, '<br />');
	challenge_message = challenge_message.replace(/&lt;/gi, '<');
	challenge_message = challenge_message.replace(/&gt;/gi, '>');

	document.getElementById("challenge_name").innerHTML = challenge_name;
	document.getElementById("challenge_message").innerHTML = challenge_message;


	document.getElementById("challenge-choice-wrapper").style.display = "inline-block";
	document.getElementById("challenge-choice-body").style.display = "inline-block";
	document.getElementById("challenge-choice-wrapper").style.zIndex = "1";
	document.getElementById("challenge-choice-body").style.zIndex = "2";
}

function challenge_choice_off(){
        document.getElementById("challenge-choice-wrapper").style.display = "none";
	document.getElementById("challenge-choice-body").style.display = "none";
}

function ChallTimer(){
	document.addEventListener("DOMContentLoaded", function() {

	// 시간을 딜레이 없이 나타내기위한 선 실행
	leftTimer();

        // 이후 0.5초에 한번씩 시간을 갱신한다.
	setInterval(leftTimer, 100);
	});
}
// 시간을 출력
function leftTimer() {
	const nowDate = new Date();
	const hour = nowDate.getHours();
	const min = nowDate.getMinutes();
	const sec = nowDate.getSeconds();

	if(24-hour < 0){
		document.getElementById("leftTimes").innerHTML = "00:00:00";
		 document.getElementById("leftTimes").style = "color : red; font-size:3em"; 
	}
	else{
		document.getElementById("leftTimes").innerHTML = (23-hour) + ":" + addzero((59-min)) + ":" + addzero(59-sec);
	}
}

// 1자리수의 숫자인 경우 앞에 0을 붙여준다.
function addzero(num) {
	if(num < 10) { num = "0" + num; }
	return num;
}

function sign_in_on(){
	document.getElementById("sign-in-wrapper").style.display = "flex";
	document.getElementById("sign-in-back").style.display = "inline-block";
}
function sign_in_off(){
	document.getElementById("sign-in-wrapper").style.display = "none";
	document.getElementById("sign-in-back").style.display = "none";
}
function sign_up_on(){
        document.getElementById("sign-up-wrapper").style.display = "flex";
        document.getElementById("sign-up-back").style.display = "inline-block";
}
function sign_up_off(){
        document.getElementById("sign-up-wrapper").style.display = "none";
        document.getElementById("sign-up-back").style.display = "none";
}

function copy_clipboard(copy_num)
{
	var clip_share = document.getElementById(copy_num);
	clip_share.select();
	document.execCommand("copy");

	clip_share.blur();

	alert("Copy Succes");


}
