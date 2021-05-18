/*
 * Check Room Codes
 * (c) Justus Languell 2021
 */

illegalCharsMsg = "Invalid Character Used!";
legalChars = '1234567890';
maxchars = 4;

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
    var code = document.getElementById('code');
    code.addEventListener('input', function usernameSafe(e)
    {
        var field = e.target;
        var legal = isLegal(field.value, field.value.length);
        if (!legal) {
            document.getElementById('codeError').innerHTML = illegalCharsMsg;
        } else {
            document.getElementById('codeError').innerHTML = "";
        }
        document.getElementById('remaining').innerHTML = field.value.length + "/" + maxchars;
    });
});

setInterval(function()
{
    var submit = document.getElementById('joinbtn');
    submit.disabled = (
    (document.getElementById('codeError').innerHTML != '')||
    ( !document.getElementById('code').value.replace(/\s/g, '').length )
    );
}, 5);

/*_*/