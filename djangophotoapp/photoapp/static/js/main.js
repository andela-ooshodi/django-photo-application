$(document).ready(function() {
    $("#flash-message").fadeOut(3000);
    // Triggers sidebar on mobile view
    $(".button-collapse").sideNav();
    // Triggers modal
    $('.modal-trigger').leanModal();
    // Upload Image on submit
    $("#upload-form").on("submit", function(event) {
        event.preventDefault();
        var fd = new FormData();
        var url = $(this).attr("action");
        var image = $(this).find("input[type='file']")[0].files[0];
        fd.append("image", image);
        upload_image(fd, url);
    });
    // AJAX for uploading image
    function upload_image(fd, url) {
        $.ajax({
            url: url,
            type: "POST",
            data: fd,
            contentType: false,
            processData: false,
            // On success
            success: function(json) {
                $(".uploaded-images").load(document.URL + " .uploaded-images", function() {
                    $('.modal-trigger').leanModal();
                });
            },
        });
    };
    // Delete Image
    $('body').on('click', '.delete-image', function() {
        var image_id = $(this).attr('id').split('-')[1];
        var url = '/home';
        delete_image(image_id, url);
    });
    // AJAX for deleting image
    function delete_image(image_id, url) {
        $.ajax({
            url: url,
            type: 'DELETE',
            data: {
                image_id: image_id
            },
            success: function(json) {
                $(".uploaded-images").load(document.URL + " .uploaded-images", function() {
                    $('.modal-trigger').leanModal();
                });
            },
        });
    };
});