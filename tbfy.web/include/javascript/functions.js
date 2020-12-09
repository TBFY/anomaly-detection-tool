
    // START :: functions managing cookie interactions
    // START :: functions managing cookie interactions

    function setCookie(name, value, hours)
    {
        var expires = "";
        if (hours)
        {
            var date = new Date();
            date.setTime(date.getTime() + (hours*60*60*1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "")  + expires + "; path=/";
    }

    function getCookie(name)
    {
        var nameEQ = name + "=";
        var ca = document.cookie.split(';');
        for(var i=0;i < ca.length;i++)
        {
            var c = ca[i];
            while (c.charAt(0)==' ') c = c.substring(1,c.length);
            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
        }
        return null;
    }

    function eraseCookie(name)
    {
        document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    }

    // END :: functions managing cookie interactions
    // END :: functions managing cookie interactions

    // START :: general functions
    // START :: general functions

    function inArray(needle, haystack)
    {
        var length = haystack.length;
        for(var i = 0; i < length; i++)
        {
            if(haystack[i] == needle)
                return true;
        }
        return false;
    }

    // END :: general functions
    // END :: general functions
