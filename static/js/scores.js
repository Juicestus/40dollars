/*
 * Score page functionality
 * (c) Justus Languell 2021
 */

var colors = ['red', 'blue', 'orange', 'purple'];

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
    scores = jQuery.parseJSON(scores);
    var users = Object.keys(scores);
    users = users.reverse();
    var colors = randomColorList(scores.length);
    render = "";
    //for (var i=0; i < users.length; i++) {
    var i=0;
    var writeScores = setInterval(function()
    {
        var user = users[i];
        //var color = colors[i];
        var color = 'purple';
        sscores = ''
        if (scores[user] <= 0) {
            sscores = 'no points';
        } else if (scores[user] == 1) {
            sscores = '1 point';
        } else {
            sscores = scores[user] + ' points';
        }
        if (user != _name) {
            user = 'You'
        }        
        if (i >=  users.length-1) {
            render = '<h1 class="' + color + '">"' + user + '" got ' + sscores + '</h1><br>' + render;
            document.getElementById('scores').innerHTML = render;
            clearInterval(writeScores);
        } else {
            render = '<h2 class="' + color + '">"' + user + '" got ' + sscores + '</h2><br>' + render;
            document.getElementById('scores').innerHTML = render;
        }
        i++;
    }, 1000);
});

/*_*/