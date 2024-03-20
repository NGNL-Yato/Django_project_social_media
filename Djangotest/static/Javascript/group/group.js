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
    button.style.backgroundColor = "#fff";
}

