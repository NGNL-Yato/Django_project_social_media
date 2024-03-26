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
function displayFile2(input) {
    console.log("displayFile2 is called");
    var fileDisplayArea = document.getElementById('Img_display');
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

document.getElementById('iconBox3Button').addEventListener('click', function(event) {
    event.stopPropagation(); // Prevent this click from triggering the document's onclick
    var profileMenu = document.getElementById('profileMenu');
    var iconBox3Button = document.getElementById('iconBox3Button');
    var rect = iconBox3Button.getBoundingClientRect();
    profileMenu.style.top = (iconBox3Button.offsetTop + rect.height) + 'px';
    profileMenu.style.left = iconBox3Button.offsetLeft + 'px';
    profileMenu.classList.toggle('show');
});

// Add an onclick event to the document that will close the dropdown
document.body.addEventListener('click', function(event) {
    var profileMenu = document.getElementById('profileMenu');
    var iconBox3Button = document.getElementById('iconBox3Button');
    if (event.target != iconBox3Button && !iconBox3Button.contains(event.target) && !profileMenu.contains(event.target)) {
        profileMenu.classList.remove('show');
    }
})

var modal = document.getElementById("myModal");
var buttons = document.getElementsByClassName("group_buttons");
var span = document.getElementsByClassName("close")[0];

Array.from(buttons).forEach((btn) => {
    btn.onclick = function() {
        modal.style.display = "block";
    }
});


var btnn = document.getElementsByClassName("event_buttons");
var eventmodal = document.getElementById("myeventModal");

Array.from(btnn).forEach((btn) => {
    btn.onclick = function() {
        console.log('clicked')
        eventmodal.style.display = "block";
        // console.log(eventmodal)
    }
});



var circleButton = document.getElementById('circleButton');
var circleMenu = document.getElementById('circleMenu');

var NotificationButton = document.getElementById('NotificationButton');
var NotificationsMenu = document.getElementById('NotificationsMenu');
NotificationButton.onclick = function() {
    console.log("Notification button clicked")
    var rect = NotificationButton.getBoundingClientRect();
    NotificationsMenu.style.top = (NotificationButton.offsetTop + rect.height) + 'px';
    NotificationsMenu.style.left = NotificationButton.offsetLeft + 'px';
    NotificationsMenu.classList.toggle('show');
}
document.body.addEventListener('click', function(event) {
    if (event.target != NotificationButton && event.target != NotificationsMenu) {
        NotificationsMenu.classList.remove('show');
    }
})
circleButton.onclick = function() {
    var rect = circleButton.getBoundingClientRect();
    circleMenu.style.top = (circleButton.offsetTop + rect.height) + 'px';
    circleMenu.style.left = circleButton.offsetLeft + 'px';
    circleMenu.classList.toggle('show');
}
document.body.addEventListener('click', function(event) {
    if (event.target != circleButton && event.target != circleMenu) {
        circleMenu.classList.remove('show');
    }
})
span.onclick = function() {
    modal.style.display = "none";
}

window.addEventListener('click', function(event) {    
    if (event.target == modal ||  event.target == eventmodal  ) {
        modal.style.display = "none";
    }
})

window.addEventListener('click', function(event) {    
    if (event.target == eventmodal  ) {
        eventmodal.style.display = "none";
    }
})


