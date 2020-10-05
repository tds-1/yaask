// nos is 0-based indexing, data is 1-based indexing
var nos;
var curr = 0;
var data = {};
const NOT_MARKED = 0;
const MARKED = 1;
const BOOKMARKED = 2;
const MARKED_BOOKMARKED = 3;
const SUBMITTED = 4;
const SUBMITTED_BOOKMARKED = 5;
var map_quest = {};
var answer = {};

$(document).ready(function () {
    var url = window.location.href;
    var list = url.split('/');
    if (url.includes('/give-test/')) {
        $.ajax({
            type: "POST",
            url: "/randomize",
            dataType: "json",
            data: { id: list[list.length - 1] },
            success: function (temp) {
                load_all_questions(temp);
                make_array();
                display_ques(1);
            }
        });
    }
    var time = parseInt($('#time').text()), display = $('#time');
    startTimer(time, display);
    sendTime();
    flag_time = true;
})


var load_all_questions = function (temp) {
    var keys = Object.keys(temp);
    map_quest = temp;
    nos = keys;
}


var unmark_all = function () {
    $('#options td').each(function (i) {
        $(this).css("background-color", 'rgba(0, 0, 0, 0)');
    });
}

var display_ques = function (move) {
    unmark_all();
    $('#que').text(map_quest[nos[move - 1]][0]);
    $('#a').text('𝐀.  ' + map_quest[nos[move - 1]][1]);
    $('#b').text('𝐁.  ' + map_quest[nos[move - 1]][2]);
    $('#c').text('𝐂.  ' + map_quest[nos[move - 1]][3]);
    $('#d').text('𝐃.  ' + map_quest[nos[move - 1]][4]);
    $('#queid').text('Question No. ' + (move));
    $('#mark').text('Marks: ' + '4');
    if (data[move].marked != null)
        $('#' + (data[move].marked)).css("background-color", 'rgba(0, 255, 0, 0.6)');

}
var flag_time = true;
function startTimer(duration, display) {
    var timer = duration, hours, minutes, seconds;

    var interval = setInterval(function () {
        hours = parseInt(timer / 3600, 10);
        minutes = parseInt((timer % 3600) / 60, 10);
        seconds = parseInt(timer % 60, 10);
        hours = hours < 10 ? "0" + hours : hours;
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.text(hours + ":" + minutes + ":" + seconds);

        if (--timer < 0) {
            finish_test();
            clearInterval(interval);
            flag_time = false;
        }
    }, 1000);
}

function finish_test() {
    $('#msg').addClass('alert-info');
    $('#msg').append("Test submitted successfully");
    $.ajax({
        type: "POST",
        dataType: "json",
        data: { flag: 'completed' },
        success: function (data) {
            window.location.replace('/dashboard');
        }
    });
}


// function sendTime() {
//     var intervalTime = setInterval(function () {
//         if (flag_time == false) {
//             clearInterval(intervalTime);
//         }
//         var time = $('#time').text();
//         var [hh, mm, ss] = time.split(':');
//         hh = parseInt(hh);
//         mm = parseInt(mm);
//         ss = parseInt(ss);
//         var seconds = hh * 3600 + mm * 60 + ss;
//         $.ajax({
//             type: 'POST',
//             dataType: "json",
//             data: { flag: 'time', time: seconds },
//         });
//         if (flag_time == false) {
//             clearInterval(intervalTime);
//         }
//     }, 5000);
// }

$(document).on('click', '#next', function (e) {
    e.preventDefault();
    curr += 1;
    if (curr >= nos.length) {
        curr -= 1;
    }
    display_ques(curr + 1);

});

$(document).on('click', '#prev', function (e) {
    e.preventDefault();
    curr -= 1;
    if (curr < 0) {
        curr = 0;
    }
    display_ques(curr + 1);

});

$('#submit').on('click', function (e) {
    e.preventDefault();
    var marked='#';
    if (flag_time == false) {
        window.location.replace('/dashboard');
        return;
    }
    var count = 0;
    $('#options td').each(function (i) {
        if ($(this).css("background-color") != 'rgba(0, 0, 0, 0)') {
            marked = $(this).attr('id');
            answer[nos[curr]] = marked
            data[curr + 1].marked = marked;
            data[curr + 1].status = SUBMITTED;
            count = count + 1;
        }
    });
    if (count == 4) {
        data[curr + 1].marked = null;
        data[curr + 1].status = NOT_MARKED;
        console.log('data')
        $.ajax({
            type: "POST",
            dataType: 'json',
            data: { flag: 'mark', qid: nos[curr], ans: marked },
        });
    }
    else{
        $.ajax({
            type: "POST",
            dataType: 'json',
            data: { flag: 'mark', qid: nos[curr], ans: marked },
        });
    }
    $('#next').trigger('click');
});

function onn() {
    $('.question').remove();
    document.getElementById("overlay").style.display = "block";
    $('#question-list').append('<div id="close">X[close]</div>');
    $('#close').on('click', function (e) {
        off();
    });
}

function off() {
    document.getElementById("overlay").style.display = "none";
    $('#close').remove();
}

$('#questions').on('click', function (e) {
    onn();
    for (var i = 1; i <= nos.length; i++) {
        var color = '';
        var status = data[i].status;
        if (status == NOT_MARKED)
            color = '#1976D2';
        else if (status == SUBMITTED)
            color = '#42ed62';
        else if (status == BOOKMARKED || status == SUBMITTED_BOOKMARKED)
            color = '#e6ed7b';
        else {
            color = '#f44336';
        }
        j = i < 10 ? "0" + i : i;
        $('#question-list').append('<div class="question" style="background-color:' + color + '; color:white;">' + j + '</div>');
    }
    $('.question').click(function () {
        var id = parseInt($(this).text());
        curr = id - 1;
        display_ques(curr + 1);
        off();
    });

});


$('#bookmark').on('click', function (e) {
    var status = data[curr + 1].status;
    if (status == MARKED)
        data[curr + 1].status = MARKED_BOOKMARKED;
    else if (status == SUBMITTED)
        data[curr + 1].status = SUBMITTED_BOOKMARKED;
    else
        data[curr + 1].status = BOOKMARKED;
});



$('#options').on('click', 'td', function () {
    if ($(this).css("background-color") != 'rgba(0, 255, 0, 0.6)') {
        var clicked = $(this).attr('id');
        var que = $('#queid').attr('id');
        unmark_all();
        $(this).css("background-color", 'rgba(0, 255, 0, 0.6)');
        data[curr + 1].status = MARKED;
        data[curr + 1].marked = $(this).attr('id');
    }
    else {
        $(this).css("background-color", 'rgba(0, 0, 0, 0)');
        data[curr + 1].status = NOT_MARKED;
        data[curr + 1].marked = null;
    }
});

var submit_overlay_display = true;
$('#finish').on("click", function (e) {
    $('#submit-overlay').empty();
    var count = marked();
    var remaining = nos.length - count;
    if (submit_overlay_display) {
        document.getElementById("submit-overlay").style.display = "block";
        $('#submit-overlay').append('<div style="background-color:white; display: inline-block;/*! margin: auto; *//*! margin: 0 auto; */position: absolute;left: 40%;top: 33%;padding: 10PX; width:30%;" align="center"><table class="table"> <tr><td>Total Questions</td><td>Attempted</td><td>Remaining</td></tr><tr><td>' + nos.length + '</td><td>' + count + '</td><td>' + remaining + '</td></tr></table> <a class="btn btn-primary" onclick="finish_test();">Submit Test</a></div>');
        submit_overlay_display = false;
    } else {
        document.getElementById("submit-overlay").style.display = "none";
        submit_overlay_display = true;
    }
});

var marked = function () {
    var count = 0;
    for (var i = 1; i <= nos.length; i++) {
        if (data[i].status == SUBMITTED || data[i].status == SUBMITTED_BOOKMARKED) {
            count++;
        }
    }
    return count;
}

var make_array = function () {
    for (var i = 0; i < nos.length; i++) {
        data[i + 1] = { marked: null, status: NOT_MARKED };
    }
    var txt = document.createElement('textarea');
    txt.innerHTML = answers;
    answers = txt.value;
    answers = JSON.parse(answers);
    for (var key in answers) {
        var store;
        for (var j = 0; j < nos.length; j++) {
            if (key == nos[j]) {
                store = j;
                break;
            }
        }
        data[store + 1].marked = answers[key]
        data[store + 1].status = SUBMITTED;
    }
}

// window.addEventListener('blur', function() { 
//     window.location.replace('/dashboard');
//  });