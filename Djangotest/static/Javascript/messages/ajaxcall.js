$(document).ready(function() {
    $.ajax({
        url: '/get_friends/', 
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            updateContactsDisplay(data.friends);
        }
    });
});

$('#show_friends').click(function() {
    $.ajax({
        url: '/get_friends/', 
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            updateContactsDisplay(data.friends);
        }
    });
});

$('#show_conversations').on('click', function() {
    $.ajax({
        url: '/get_friends/', 
        type: 'GET',
        success: function(data) {
            // Clear the current display
            $('.contacts_display').empty();
            // Display the group conversations
            data.group_conversations.forEach(function(conversation) {
                var conversationElement = '<li>' +
                                        '<div class="user_friend_displayed">' +
                                        '<div class="img_cont">' +
                                        '<img src="' + conversation.picture + '" class="user_img">' +
                                        '<span class="online_icon"></span>' +
                                        '</div>' +
                                        '<div class="user_info">' +
                                        '<span data_username="' + conversation.title + '">' + conversation.title + '</span>' +
                                        '<p>Online</p>' +
                                        '</div>' +
                                        '</div>' +
                                        '</li>';
                $('.contacts_display').append(conversationElement);
            });
        }
    });
});
function updateContactsDisplay(friends) {
    var contactsDisplay = $('.contacts_display');
    contactsDisplay.empty();
    for (var i = 0; i < friends.length; i++) {
        var friend = friends[i];
        var friendHTML = '<li>' +
            '<div class="user_friend_displayed">' +
            '<div class="img_cont">' +
            '<img src="' + friend.profile_picture + '" class="user_img">' +
            '<span class="online_icon"></span>' +
            '</div>' +
            '<div class="user_info">' +
            '<span data_username='+friend.username+'>' + friend.first_name + ' ' + friend.last_name + '</span>' +
            '<p>Online</p>' +
            '</div>' +
            '</div>' +
            '</li>';

        // Append the friend HTML to the contacts display
        contactsDisplay.append(friendHTML);
    }
}

$('.search_bar').on('keyup', function() {
    var value = $(this).val().toLowerCase();
    $(".contacts_display .user_friend_displayed").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});
$(document).on('click', '.user_friend_displayed', function() {
    // Remove the 'active' class from all 'li' elements
    $('li.active').removeClass('active');
    // Add the 'active' class to the 'li' that contains the clicked 'div'
    $(this).closest('li').addClass('active');
    var username = $(this).find('.user_info span').attr('data_username');
    var profilePicture = $(this).find('.img_cont img').attr('src');
    var friendPicture = $('#friend_picture').attr('src');
    $('.message_header .user_info span').text(username);
    $('.message_header .img_cont img').attr('src', profilePicture);
    $('.message_box').empty();
    $('.chat-messages').show();
    $.ajax({
        url: '/get_or_create_conversation/', 
        type: 'POST',
        data: {
            'username': username
        },
        success: function(data) {
            console.log('Setting conversation ID: ' + data.conversation);
            // Store the conversation ID in a hidden input field
            $('#conversation_id').val(data.conversation);
            var userPicture = data.user_picture;
            var friendPicture = data.friend_picture;
            data.messages.forEach(function(message) { // Remove the index parameter
                // Display the message
                var content = message.content; // Get the message content from the server response
                var sender = message.is_user_sender ? 'sender' : 'receiver'; // Determine the sender based on is_user_sender
                var timestamp = message.timestamp; // Get the timestamp from the server response
                console.log("Image :" + message.file_urls) // Access file_url from the message object
                displayMessage(content, 'sender', userPicture, friendPicture, timestamp, message.file_url); // Use file_url from the message object
            });
        }
    });
});

$('.input-group-text-bt2').on('click', function() {
    var message = $('.message_input_box textarea').val();
    var conversationId = $('#conversation_id').val();
    var fileInput = document.getElementById('fileInput');
    var file = fileInput.files[0];
    var formData = new FormData();
    formData.append('message', message);
    formData.append('conversation', conversationId);
    formData.append('file', file);
    var userPicture, friendPicture;
    $.ajax({
        url: '/get_friends/', 
        type: 'GET',
        success: function(data) {
            userPicture = data.user_picture;
            friendPicture = data.friends[0].profile_picture;
            $.ajax({
                url: '/send_message/', 
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(data) {
                    $('#messagearea').val('');
                    $('#fileInput').val('');
                    // If you want to access the first file URL
                    var firstFileUrl = data.file_urls[0];
                    displayMessage(message, 'sender', userPicture, friendPicture, new Date().toLocaleTimeString(), firstFileUrl);
                    console.log(fileInput.files[0])
                    console.log('Message sent');
                }
            });
        
        }
    });
});

function displayMessage(message, sender, userPicture, friendPicture, timestamp, fileUrl) {
    console.log("Message :" + message)
    var messageContainer;
    var imgCont = $('<div>').addClass('img_cont_msg');
    var img;
    var msgContainer = $('<div>').addClass(sender === 'receiver' ? 'msg_container' : 'msg_container_send');
    var msgTime = $('<span>').addClass(sender === 'receiver' ? 'msg_time' : 'msg_time_send');

    if (sender === 'receiver') {
        messageContainer = $('<div>').addClass('message_container_receiver');
        img = $('<img>').attr('src', friendPicture).addClass('user_img_msg');
    } else {
        messageContainer = $('<div>').addClass('message_container_sender');
        img = $('<img>').attr('src', userPicture).addClass('user_img_msg');
    }

    imgCont.append(img);
    msgContainer.text(message);

    var messageDate = new Date(timestamp);
    var currentDate = new Date();

    // Check if the message date and the current date are the same
    if (messageDate.toDateString() === currentDate.toDateString()) {
        // If the dates are the same, only display the time
        msgTime.text(messageDate.toLocaleTimeString());
    } else {
        // If the dates are different, display the date
        msgTime.text(messageDate.toLocaleDateString());
    }

    msgContainer.append(msgTime);

    if (fileUrl) {
        console.log("FileUrl :" + fileUrl)
        var fileImg = $('<img>').attr('src', fileUrl).css({
            width: '100px',
            height: '100px'
        });
        fileImg.on('load', function() {
            // The image has loaded successfully
            msgContainer.prepend(fileImg);
            msgContainer.append($('<br>'));
        });
    }
    if (sender === 'receiver') {
        messageContainer.append(imgCont);
        messageContainer.append(msgContainer);
    } else {
        messageContainer.append(msgContainer);
        messageContainer.append(imgCont);
    }

    $('.message_box').append(messageContainer);
    $('.message_box').scrollTop($('.message_box')[0].scrollHeight);
}
$('#fileInput').on('change', function() {
    var previewContainer = $('#previewContainer');
    previewContainer.empty();
    var fileInput = this;
    for (var i = 0; i < this.files.length; i++) {
        (function(i) {
            var file = fileInput.files[i];
            var reader = new FileReader();
            reader.onload = function(e) {
                var preview = $('<img>').attr('src', e.target.result).css({
                    width: '100px',
                    height: '100px'
                });
                var closeButton = $('<i class="fa-solid fa-rectangle-xmark">').css({
                    position: 'absolute',
                    top: '0',
                    right: '0',
                    cursor: 'pointer'
                }).on('click', function() {
                    $(this).parent().remove();
                    var dt = new DataTransfer();
                    $.each(fileInput.files, function(j, f) {
                        if (j != i) {
                            dt.items.add(f);
                        }
                    });
                    fileInput.files = dt.files;
                    if (fileInput.files.length === 0) {
                        previewContainer.hide(); // Hide the preview container if there are no more files
                    }
                });
                var previewWrapper = $('<div>').css({
                    position: 'relative',
                    display: 'inline-block'
                }).append(closeButton, preview);
                previewContainer.append(previewWrapper).show(); // Show the preview container when adding content
            }
            reader.readAsDataURL(file);
        })(i);
    }
});