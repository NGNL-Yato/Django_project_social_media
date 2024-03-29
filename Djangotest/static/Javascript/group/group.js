let groupButtons = document.getElementsByClassName('group-buttons');


// Apply JS hover and exit methods on the elements of the group-buttons class
Array.from(groupButtons).forEach(groupButton => {
    let buttons = groupButton.children;
    Array.from(buttons).forEach(button => {
        button.onmouseover = function() {
            Mousehover(this);
        };
        button.onmouseout = function() {
            exit(this);
        }
    });
});

// Change the color of the button when the mouse is over it
function Mousehover(target) {
    let button = target;
    button.children[0].style.color = "#fff";
    button.style.color = "#fff";
    button.style.backgroundColor = "#8c79a9";   
}

// Change the color of the button when the mouse is not over it
function exit(target) {
    let button = target;
    button.children[0].style.color = "#8c79a9";
    button.style.backgroundColor = "var(--white)";
}
// When the user clicks on "Invite people", open the modal
document.getElementById('invite_button').addEventListener('click', function() {
    document.querySelector('#home_settings').style.display = 'block';
});

// When the user clicks anywhere outside of the modal, close it
window.addEventListener('mousedown', function(event) {
    console.log('up')
    var modal = document.querySelector('#home_settings');
    if (!modal.contains(event.target) && event.target.id !== 'invite_button') {
        modal.style.display = 'none';
    }
});
// When the user clicks on the "x" button, close the modal
document.querySelector('.close').addEventListener('click', function() {
    document.querySelector('#home_settings').style.display = 'none';
});
//When user click on the settings buttons
document.querySelector('#settings_bt').addEventListener('click', function() {
    window.location.href = this.getAttribute('href');
});