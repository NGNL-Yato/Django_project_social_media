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

$('#show_conversations').click(function() {
    // Fetch the user and friend pictures before sending the message
    $.ajax({
        url: '/get_friends/', 
        type: 'GET',
        success: function(data) {
            // Assuming the logged-in user is the first one in the friends array
            var userPicture = data.friends[0].profile_picture;
            // Assuming the friend is the second one in the friends array
            var friendPicture = data.friends[1].profile_picture;

            // Now send the message
            $.ajax({
                url: '/send_message/', 
                type: 'POST',
                data: {
                    'message': message,
                    'conversation': conversationId
                },
                success: function(data) {
                    console.log(data);
                    displayMessage(message, 'sender', userPicture, friendPicture);
                    console.log('Message sent');
                }
            });
        }
    });
});
function updateContactsDisplay(friends) {
    var contactsDisplay = $('.contacts_display');
    contactsDisplay.empty();
    for (var i = 0; i < friends.length; i++) {
        var friend = friends[i];
        var friendHTML = '<li class="active">' +
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

function updateConversationsDisplay(friendConversations, groupConversations) {
    var conversationsDisplay = $('.contacts_display');
    conversationsDisplay.empty(); 
    for (var i = 0; i < friendConversations.length; i++) {
        var conversation = friendConversations[i];
        var conversationHTML = generateConversationHTML(conversation);
        conversationsDisplay.append(conversationHTML);
    }
    for (var i = 0; i < groupConversations.length; i++) {
        var conversation = groupConversations[i];
        var conversationHTML = generateConversationHTML(conversation);
        conversationsDisplay.append(conversationHTML);
    }
}

function generateConversationHTML(conversation) {
    return '<li class="active">' +
        '<div class="conversation_displayed">' +
        '<div class="img_cont">' +
        '<img src="' + conversation.picture + '" class="conversation_img">' +
        '</div>' +
        '<div class="conversation_info">' +
        '<span>' + conversation.title + '</span>' +
        '</div>' +
        '</div>' +
        '</li>';
}
$('.search_bar').on('keyup', function() {
    var value = $(this).val().toLowerCase();
    $(".contacts_display .user_friend_displayed").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});
$(document).on('click', '.user_friend_displayed', function() {
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
            data.messages.forEach(function(message) {
                // Display the message
                var content = message.content; // Get the message content from the server response
                var sender = message.is_user_sender ? 'sender' : 'receiver'; // Determine the sender based on is_user_sender
                var timestamp = message.timestamp; // Get the timestamp from the server response
                displayMessage(content, sender, userPicture, friendPicture,timestamp);
            });
        }
    });
});

$('.input-group-text-bt2').on('click', function() {
    var message = $('.message_input_box textarea').val();
    var conversationId = $('#conversation_id').val();
    console.log('Retrieved conversation ID: ' + conversationId);
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
                data: {
                    'message': message,
                    'conversation': conversationId
                },
                success: function(data) {
                    console.log(data);
                    displayMessage(message, 'sender', userPicture, friendPicture);
                    $('.message_input_box textarea').val('');
                }
            });
        }
    });
});

function displayMessage(message, sender, userPicture, friendPicture, timestamp) {
    console.log(userPicture)
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

    if (sender === 'receiver') {
        messageContainer.append(imgCont);
        messageContainer.append(msgContainer);
    } else {
        messageContainer.append(msgContainer);
        messageContainer.append(imgCont);
    }

    $('.message_box').append(messageContainer);
}