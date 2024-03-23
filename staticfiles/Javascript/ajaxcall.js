$('.like-button').click(function() {
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