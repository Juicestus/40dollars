/*
 * Game page functionality
 * (c) Justus Languell 2021
 */

var allowedExt = ['png','jpeg','jpg','gif'];

function b64size(src) 
{
    return Math.round(4 * Math.ceil(((src.length - 22) / 3)) * 0.5624896334383812);
}

function isFileGood(name)
{
    var fextg = false;
    var splitName = name.split('.')
    for (var ext of allowedExt) {
        if (splitName[splitName.length-1] == ext) {
            fextg = true
        }
    }
    return fextg
}
function sendImg()
{
    var file = document.getElementById('fileUpload').files[0];
    document.getElementById('fileUpload').type = "text";
	document.getElementById('fileUpload').type = "file";
    var reader = new FileReader();
    reader.onloadend = function() {
        src = reader.result;
        var size = b64size(src);
        if (size < 8e6) {
            socket.emit('imgSubmit',
            {	
                code: code,
                name: _name,
                round: round,
                host: host,
                src: src
            });
        } else {
            document.getElementById('warning').innerHTML = "Image excedes 8mb max file size!";
        }
    };
    if (file) {
        console.log(isFileGood(file.name))
        if (isFileGood(file.name)) {
            document.getElementById('warning').innerHTML = "";
            reader.readAsDataURL(file);
        } else {
            document.getElementById('warning').innerHTML = "Not an allowed image type!";
        }
    } else {
        document.getElementById('warning').innerHTML = "No image selected!";
        /*
        socket.emit('imgSubmit',
        {	
            code: code,
            name: _name,
            round: round,
            host: host,
            src: 'NOIMAGE'
        });
        */
    }
}

function sendstart() 
{
    socket.emit('adminOverideSub', {	
        code: code,
        name: _name,
        round: round,
        host: host
    });
}

$(document).ready(function() 
{
    if (host == _name) {
        
        document.getElementById('start').innerHTML = 
        ('<br><div class="btn-wrap upl-btn-wrap">' +
        `<button type="button" class="btn" onclick="sendstart();"><h3>Skip to vote</h3></button><br>` +
        '</div>');
    }

    setInterval(function() 
    {
        var fn = document.getElementById('fileUpload').files[0];
        if (typeof fn == "undefined") {
            fn = "No image file selected yet"
        } else {
            fn = fn.name;
        }
        document.getElementById('imageName').innerHTML = fn;
    }, 100);

    socket.emit('needSubbedPlayers',
    {	
        code: code,
        name: _name,
        round: round,
        host: host
    });

    socket.emit('needPrompt',
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

    socket.on('playerSubbed', function(subbedPlayers)
    {   
        var subbedUsers = Object.keys(subbedPlayers);
        whosDone = "";
        for (var user of subbedUsers) {
            whosDone += '<h4 class="blue">"' + user + '" is done!</h4><br>'
        }
        document.getElementById('subbed').innerHTML = whosDone;
    }); 

    socket.on('allPlayersSubbed', function(p)
    {   
        //window.location.replace('/play/' + code + '/' + (round+1));
        location.replace('/play/' + code + '/game');
    }); 
});

/*_*/