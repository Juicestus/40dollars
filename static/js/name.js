/*
 * Check Names
 * (c) Justus Languell 2021
 */

illegalCharsMsg = "Invalid Character Used!";
legalChars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.';
maxchars = 12;

function isLegal(s,l)
{
    legal = true;
    for (var i=0; i<l; i++) {
        charLegal = false;
        if (!legalChars.includes(s[i])) {        
            legal = false;
        }
    }
    return legal;
};

$(document).ready(function() 
{
    var name = document.getElementById('name');
    name.addEventListener('input', function usernameSafe(e)
    {
        var field = e.target;
        var legal = isLegal(field.value, field.value.length);
        if (!legal) {
            document.getElementById('nameError').innerHTML = illegalCharsMsg;
        } else {
            document.getElementById('nameError').innerHTML = "";
        }
        document.getElementById('remaining').innerHTML = field.value.length + "/" + maxchars;
    });
});

setInterval(function()
{
    var submit = document.getElementById('joinbtn');
    submit.disabled = (
    (document.getElementById('nameError').innerHTML != '')||
    ( !document.getElementById('name').value.replace(/\s/g, '').length )
    );
}, 5);

/*_*/