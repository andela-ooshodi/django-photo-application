$(document).ready(function () {
    $("#flash-message").fadeOut(3000);
    $(".button-collapse").sideNav();

    // Upload Image on submit
    $("#upload-form").on("submit", function(event) {
        event.preventDefault();
        var fd = new FormData();
        var url = $(this).attr("action");
        var image = $(this).find('input[type="file"]')[0].files[0];
        fd.append("image", image);
        // var other_data = $(this).serializeArray();
        // $.each(other_data, function(key, input) {
        //     fd.append(input.name, input.value);
        // });
        upload_image(fd, url);
    });
    // AJAX for uploading image
    function upload_image(fd, url) {
        $.ajax({
            url: url,
            type: "POST",
            data: fd,

            // On success
            success: function(json) {
                    $(".uploaded-images").load(document.URL + " .uploaded-images");
                },
        });
    };
});