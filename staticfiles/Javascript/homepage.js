var darkButton = document.querySelector(".darkTheme");
darkmodeactivate = false

darkButton.onclick = function(){
    darkButton.classList.toggle("button-Active");
    document.body.classList.toggle("dark-color");
    console.log("Dark mode is active");
    if ( darkmodeactivate == false){
        darkmodeactivate = true
        var textColor = document.querySelectorAll(".heading")
        textColor.style.color = "white"
        console.log ("dark mode up")
        console.log (textColor)
    } else {
        darkmodeactivate = false
        console.log ("dark mode down")
    }   
}

