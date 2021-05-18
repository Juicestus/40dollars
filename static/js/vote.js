/*
 * Voting page functionality
 * (c) Justus Languell 2021
 */

var vote = 'NONE';
var colors = ['red', 'blue', 'orange', 'purple'];

function shuffle(array) 
{
    var currentIndex = array.length, temporaryValue, randomIndex;
  
    while (0 !== currentIndex) {
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;
    
        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
    }
    return array;
}

function getRandomInt(max) 
{
    return Math.floor(Math.random() * max);
}

function randomColorList(len)
{
    randcolors = [colors[getRandomInt(colors.length)]];
    for (var i=0; i < len-1; i++) {
        do {
            newcolor = colors[getRandomInt(colors.length)];
        } while (newcolor == randcolors[randcolors.length - 1]);
        randcolors.push(newcolor);
    }
    return randcolors;
}

$(document).ready(function() 
{
    /* Get time update interval */
    var tinterv = setInterval(function() 
    {
        socket.emit('getTimer',
        {	
            code: code,
            name: _name,
            round: round,
            host: host
        });
    }, 250);

    socket.emit('needPrompt',
    {	
        code: code,
        name: _name,
        round: round,
        host: host
    });
    socket.emit('getImagesForVote',
    {	
        code: code,
        name: _name,
        round: round,
        host: host
    });

    socket.on('promptLoad', function(_prompt)
    {   
        document.getElementById('prompt').innerHTML = _prompt;
    }); 
    
    socket.on('timerUpdate', function(resp)
    {   
        s = resp.state;
        t = parseInt(resp.endtime);

        if (s == 'A') {
            document.getElementById('timer').innerHTML = t-10 - Math.round((new Date()).getTime() / 1000);
        } else if (s == 'B') {
            socket.emit('getVotes',
            {	
                code: code,
                name: _name,
                round: round,
                host: host
            });
            document.getElementById('timer').innerHTML = t - Math.round((new Date()).getTime() / 1000);
        } else if (s == 'C') {
            location.reload();
        }
    }); 

    socket.on('displayVotes', function(votes)
    {
        //document.getElementById('timer').innerHTML = "Counting Votes!";
        var users = Object.keys(votes);
        var colors = randomColorList(users.length);
        render = "";
        for (var i=0; i < users.length; i++) {
            var user = users[i];
            //var color = colors[i];
            var color = 'purple';
            svotes = ''
            if (votes[user] <= 0) {
                svotes = 'no votes';
            } else if (votes[user] == 1) {
                svotes = '1 vote';
            } else {
                svotes = votes[user] + ' votes';
            }
            if (user != _name) {
                document.getElementById('vote_' + user).innerHTML = '<h2 class="' + color + '">"' + user + '"<br> got ' + svotes + '</h2>';
            } else {
                document.getElementById('vote_' + user).innerHTML = '<h2 class="' + color + '">You<br> got ' + svotes + '</h2>';
            }
        }
    });

    socket.on('imagesForVote', function(images)
    {   
        var users = Object.keys(images);
        users = shuffle(users);
        var colors = randomColorList(users.length);
        render = "";
        for (var i=0; i < users.length; i++) {
            var user = users[i];
            //var color = colors[i];
            var button = '<h3 class="blue">You cant vote 4<br> urself, silly!</h3>';
            var color = 'orange';
            if (user != _name) {
                button = '<button id="vote' + i + '" class="btn votebtn" onclick="voteFor(this.id, ' + "'" + _name + "'" + ', '+ "'" + user + "'" + ')"><h4 class="' + color + '">Vote!</button>';
            }
            if (i % 2 == 0) {
                render += '<tr><td><div class="vote"><img src="' + images[user] + '"></div></td><td><div class="vote" id="vote_' + user + '">' + button + '<div></td></tr>';
            } else {
                render += '<tr><td><div class="vote"><img src="' + images[user] + '"></div></td><td><div class="vote" id="vote_' + user + '">' + button + '<div></td></tr>';
            }
        } 
        document.getElementById('images').innerHTML = render;
    }); 
});

function voteFor(id, _name, user)
{
    if ($('#' + id).hasClass('voteSelected')) {
        $('#' + id).removeClass('voteSelected');
    } else {
        if ($('.voteSelected').length < 1) {
            $('#' + id).addClass('voteSelected');
        } else {
            for (var i=0; i < $('.votebtn').length; i++) {
                //if ($('#' + i).hasClass('voteSelected')) {
                    $('#vote' + i).removeClass('voteSelected');
                //}
            }
            $('#' + id).addClass('voteSelected');
        }
        socket.emit('sendVote',
        {	
            code: code,
            name: _name,
            round: round,
            host: host,
            vote: user
        });
    }
}

/*_*/