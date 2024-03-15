var darkButton = document.querySelector(".darkTheme");
var darkmodeactivate = false;

darkButton.onclick = function(){
    darkButton.classList.toggle("button-Active");
    document.body.classList.toggle("dark-color");
    console.log("Dark mode is active");
    if (darkmodeactivate == false){
        darkmodeactivate = true
        var textColors1 = document.querySelectorAll(".heading")
        var textColors2 = document.querySelectorAll(".explore a")
        console.log(textColors1)
        textColors1.forEach(function(textColor) {
            textColor.style.color = "white";
        });
        console.log(textColors2)
        textColors2.forEach(function(textColor) {
            textColor.style.color = "white";
        });
        console.log("dark mode up");
    } else {
        darkmodeactivate = false;
        console.log("dark mode down");
    }   
}
document.getElementById('iconBox3Button').addEventListener('click', function() {
    document.getElementById('profileMenu').classList.toggle('show');
});