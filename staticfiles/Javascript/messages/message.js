document.addEventListener('DOMContentLoaded', function() {
    var actionMenuBtn = document.getElementById('checkbox');

    actionMenuBtn.addEventListener('click', function() {
        var actionMenu = document.getElementById('action_menu');
        var displayStyle = window.getComputedStyle(actionMenu).display;
        if (displayStyle === 'none') {
            actionMenu.style.display = 'block';
        } else {
            actionMenu.style.display = 'none';
        }
    });
});