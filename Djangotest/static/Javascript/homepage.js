var darkButton = document.querySelector(".darkTheme");
var darkmodeelements = {}
var heading = document.getElementsByClassName("create-page ul li button heading",".messenger-search","fa-user-group","event .button","friend ul li button","explore a","see-more-btn")
darkmodeactivate = false

darkButton.onclick = function(){
    darkButton.classList.toggle("button-Active");
    document.body.classList.toggle("dark-color");
    darkmodeelements = heading
    for (var i = 0; i < darkmodeelements.length; i++) {
        darkmodeelements[i].classList.toggle("dark-color");
    }
    console.log("Dark mode is active");
    console.log(darkmodeelements)
    if ( darkmodeactivate == false){
        darkmodeactivate = true
        console.log ("dark mode up")
    } else {
        darkmodeactivate = false
        console.log ("dark mode down")
    }   
}

