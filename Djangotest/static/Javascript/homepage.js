var darkButton = document.querySelector(".darkTheme");
var darkmodeactivate = false;

document.getElementsByClassName('website-name')[0].addEventListener('click', function() {
    window.location.href = this.getAttribute('data-url');
});
function displayFile(input) {
    var fileDisplayArea = document.getElementById('file-display');
    var file = input.files[0];
    if (file) {
        var reader = new FileReader();
        reader.onload = function(e) {
            fileDisplayArea.innerHTML = '<img src="' + e.target.result + '" style ="height: 20%; width: 20%;">';
        }
        reader.readAsDataURL(file);
    }
}

const heartIcon = document.querySelectorAll(".like-button .heart-icon");
const likesAmountLabel = document.querySelectorAll(".like-button .likes-amount");

heartIcon.forEach((icon) => {
    icon.addEventListener("click", () => {
        icon.classList.toggle("liked");
    });
});
function toggleLike(element) {
    var heartIcon = element.querySelector('.heart-icon');
    heartIcon.classList.toggle('liked');
}

darkButton.onclick = function(){
    darkButton.classList.toggle("button-Active");
    document.body.classList.toggle("dark-color");
    console.log("Dark mode is active");
    var textColors1 = document.querySelectorAll(".heading")
    var textColors2 = document.querySelectorAll(".explore a")
    if (darkmodeactivate == false){
        darkmodeactivate = true
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
        textColors1.forEach(function(textColor) {
            textColor.style.color = "#6524c4";
        });
        console.log(textColors2)
        textColors2.forEach(function(textColor) {
            textColor.style.color = "#6524c4";
        });
        console.log("dark mode down");
    }   
}

console.log("Homepage.js loaded")

document.getElementById('iconBox3Button').addEventListener('click', function() {
    var profileMenu = document.getElementById('profileMenu');
    var iconBox3Button = document.getElementById('iconBox3Button');
    var rect = iconBox3Button.getBoundingClientRect();
    profileMenu.style.top = (iconBox3Button.offsetTop + rect.height) + 'px'; // Adjusted this line
    profileMenu.style.left = iconBox3Button.offsetLeft + 'px'; // Adjusted this line
    profileMenu.classList.toggle('show');
});
