$(document).on('click', '.like-button', function() {
    var postId = $(this).data('post-id');
    var likeButton = $(this);
    $.ajax({
        url: '/like_post/' + postId + '/',
        method: 'POST',
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(data) {
            $('.like-button[data-post-id="' + postId + '"] .likes-amount').text(data.likes);
            if (data.liked) {
                likeButton.addClass('liked');
            } else {
                likeButton.removeClass('liked');
            }
        }
    });
});

$(document).ready(function() {
    $('.like-button').each(function() {
        var postId = $(this).data('post-id');
        var likesAmountElement = $(this).find('.likes-amount');
        $.ajax({
            url: '/like_post/' + postId + '/',
            method: 'GET',
            success: function(data) {
                likesAmountElement.text(data.likes);
            }
        });
    });
});
$('#search-input').on('input', function() {
    var query = $(this).val();
    if (query.length > 0) {  // Only make the AJAX call if the input field is not empty
        $.ajax({
            url: '/search_people/',
            data: {
                'query': query
            },
            success: function(data) {
                console.log(data);
                var results = '';
                if (data.length === 0) {
                    results = 'No person with this name';
                } else {
                    $.each(data, function(index, person) {
                        results += '<p>' + person.first_name + ' ' + person.last_name + '<button class="invite-button" data-username="' + person.username + '" style="border: none; background: none; padding: 0; transition: transform 0.3s ease; margin-inline-start: 5%;"><i class="fa-solid fa-plus"></i></button></p>';
                    });
                }
                $('#search-results').html(results);
            }
        });
    } else {
        $('#search-results').html('');  // Clear the results when the input field is empty
    }
});
$(document).on('click', '.invite-button', function() {
    var username = $(this).data('username');
    var groupName = window.location.pathname.split('/')[2];
    $.ajax({
        url: '/invite_user/',
        method: 'POST',
        data: {
            'username': username,
            'group_name': groupName
        },
        success: function(response) {
            alert(response.message);
        }
    });
});
