function toggle_control(){
    toggle = document.getElementById("flexSwitchCheckDefault")

    if (toggle.checked){
        document.cookie = "on_eye=" + toggle.checked + ";path=/";
    }
    else {
        document.cookie = "on_eye=" + toggle.checked  + ";path=/";
    }
    
    select_css(toggle.checked)
}

function toggle_cookie(){
    var arrayCookie = document.cookie.split(";");
    toggle = document.getElementById("flexSwitchCheckDefault")

    if(arrayCookie[arrayCookie.indexOf(" on_eye=false")]){
        toggle.checked = false
    }

    if(arrayCookie[arrayCookie.indexOf(" on_eye=true")]){
        toggle.checked = true
    }
    
    select_css(toggle.checked)
}

toggle_cookie()

function select_css(togle_checked){

    css_body = document.getElementById("body_css")

    if (togle_checked){
        css_body.style.cssText = 
        `
            background-image: url("/static/media/eye.gif");
        `;
    }
    else{
        css_body.style.cssText = 
        `
            background: #333;
        `;
    }

}