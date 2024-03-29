$.ajax({
    url: '/get_friends/',  // Update with the correct URL
    type: 'GET',
    dataType: 'json',
    success: function(data) {
        updateContactsDisplay(data.friends);
        updateConversationsDisplay(data.conversations);
    }
});
function updateContactsDisplay(friends) {
    var contactsDisplay = $('.contacts_display');
    contactsDisplay.empty();  // Clear the current display

    // Loop through the friends data and create HTML for each friend
    for (var i = 0; i < friends.length; i++) {
        var friend = friends[i];
        var friendHTML = '<li class="active">' +
            '<div class="user_friend_displayed">' +
            '<div class="img_cont">' +
            '<img src="' + friend.profile_picture + '" class="user_img">' +
            '<span class="online_icon"></span>' +
            '</div>' +
            '<div class="user_info">' +
            '<span>' + friend.first_name + ' ' + friend.last_name + '</span>' +
            '<p>Online</p>' +
            '</div>' +
            '</div>' +
            '</li>';

        // Append the friend HTML to the contacts display
        contactsDisplay.append(friendHTML);
    }
}

function updateConversationsDisplay(conversations) {
    var conversationsDisplay = $('.conversations_display');
    conversationsDisplay.empty();  // Clear the current display

    // Loop through the conversations data and create HTML for each conversation
    for (var i = 0; i < conversations.length; i++) {
        var conversation = conversations[i];
        var conversationHTML = '<li class="active">' +
            '<div class="conversation_displayed">' +
            '<div class="img_cont">' +
            '<img src="' + conversation.picture + '" class="conversation_img">' +
            '</div>' +
            '<div class="conversation_info">' +
            '<span>' + conversation.title + '</span>' +
            '</div>' +
            '</div>' +
            '</li>';

        // Append the conversation HTML to the conversations display
        conversationsDisplay.append(conversationHTML);
    }
}