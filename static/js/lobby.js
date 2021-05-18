/*
 * Lobby page functionality
 * (c) Justus Languell 2021
 */

var colors = ['red', 'blue', 'green', 'orange', 'purple'];

function sendstart() 
{
    socket.emit('startGame', {	
        code: code,
        name: _name,
        host: host
    });
}

$(document).ready(function() 
{
    if (host == _name) {
        document.getElementById('start').innerHTML = 
        ('<br><div class="btn-wrap upl-btn-wrap">' +
        `<button type="button" class="btn" onclick="sendstart();"><h3>Start Game</h3></button><br>` +
        '</div>');
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

    socket.emit('newPlayerJoin',
    {	
        code: code,
        name: _name
    });
    
    socket.on('serverUpdatePlayers', function(players)
	{
        var players = Array.from(players);
        var randcolors = randomColorList(players.length);
        render = "";
        for (var i=0; i < players.length; i++) { 
            var player = players[i];
            var color = randcolors[i];
            render += '<b class="' + color + '">' + player; 
            if (player == host) {
                render += '&nbsp;<i style="font-size: 36px;">(host)</i>';
            }
            if (i == players.length-1) {
                render += '</b><br> ';
            } else {
                render += ',</b><br> ';
            }
        }
        document.getElementById('players').innerHTML = render;
    });

    socket.on('serverCantStartGame', function(issue)
	{   
        document.getElementById('startissue').innerHTML = '<br>' + issue;
    });

    socket.on('serverStartGame', function()
	{   
        location.replace('/play/' + code + '/game');
    });
});

/*_*/