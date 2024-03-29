$(document).ready(function() {
    $.ajax({
        url: '/get_friends/',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            updateContactsDisplay(data);
        }
    });
});