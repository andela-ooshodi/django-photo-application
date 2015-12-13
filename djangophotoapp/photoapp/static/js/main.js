$(document).ready(function() {
    ///////////// Load FB JS SDK asynchronously
    $.getScript("//connect.facebook.net/en_US/sdk.js", function() {
        FB.init({
            appId: "1531263510520883",
            version: "v2.5"
        });
    });
    /////////////////////////////////////////////////////

    $("#flash-message").fadeOut(3000);
    // Triggers sidebar on mobile view
    $(".button-collapse").sideNav();
    // Triggers modal
    $(".modal-trigger").leanModal();
    // Make the input file empty
    $("#img-file").val("");
    $("#img-file-path").val("");
    $("#upload-form-mobile #img-file").val("");
    $("#upload-form-mobile #img-file-path").val("");


    // Display the upload button after file has been attached
    $("#img-file").on("change", function() {
        $(".file-input").css("display", "none");
        $("#upload-button-lg").css("display", "block");
        $("#upload-form").css("margin-bottom", "20px");
    });

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
        $(".preloader-wrapper").css("display", "block");
        $.ajax({
            url: url,
            type: "POST",
            data: fd,
            contentType: false,
            processData: false,
            // On success
            success: function(json) {
                $(".preloader-wrapper").css("display", "none");
                Materialize.toast("Upload Successful!", 4000);
                $(".uploaded-images").load(document.URL + " .uploaded-images", function() {
                    $(".modal-trigger").leanModal();
                    $("#img-file").val("");
                    $("#img-file-path").val("");
                    $(".file-input").css("display", "block");
                    $("#upload-button-lg").css("display", "none");
                    $("#upload-form").css("margin-bottom", "50px");
                });
            },
            error: function(status) {
                $(".preloader-wrapper").css("display", "none");
                $("#img-file").val("");
                $("#img-file-path").val("");
                Materialize.toast("Invalid File Input!", 4000);
            }
        });
    };

    // Delete Image
    $("body").on("click", ".delete-image", function() {
        var image_id = $(this).attr("id").split("-")[1];
        var url = "/home";
        $("#section-" + image_id).hide();
        $("#divider-" + image_id).hide();
        delete_image(image_id, url);
    });
    // AJAX for deleting image
    function delete_image(image_id, url) {
        $.ajax({
            url: url,
            type: "DELETE",
            data: {
                image_id: image_id
            },
            success: function(json) {
                Materialize.toast("Delete Successful!", 4000);
                $(".uploaded-images").load(document.URL + " .uploaded-images", function() {
                    $(".modal-trigger").leanModal();
                });
            },
        });
    };

    // Focus the image to the center of page
    $("body").on("click", ".edit", function() {
        var img_id = $(this).attr("id").split("-")[1];
        var img_publicid = $("#img-" + img_id).attr("src").split("/")[5]
        $("#img").attr("src", "http://res.cloudinary.com/myphotoapp/" + img_publicid);
        var img_src = $("#img").attr("src");
        $("#canvas").css("display", "block");
        $("#canvas").css("margin", "auto");
        filter(img_src);
    });

    // Reset the canvas with the current image
    $("#resetbtn").on("click", function(e) {
        var current_img = $("#img").attr("src");
        filter(current_img);
    });

    // Share image
    $("#sharebtn").on("click", function(e) {
        var canvas = document.getElementById('canvas');
        var img_dataURL = canvas.toDataURL('image/jpeg', 0.1);
        upload_edited_image(img_dataURL);
    });
    // AJAX for uploading edited image
    function upload_edited_image(img_dataURL) {
        console.log(img_dataURL);
        $("#preloadershare").css("display", "inline-block");
        $.ajax({
            url: "/upload",
            type: "POST",
            data: { 
                imgBase64: img_dataURL
            },
            // On success
            success: function(json) {
                FB.ui({
                    method: "feed",
                    link: location.href,
                    caption:"myPhotoApp",
                    picture: json.url,
                    description: "I just used myPhotoApp to edit this photo and I love it."
                },function(response){});
                $("#preloadershare").css("display", "none");
            },
            error: function(status) {
                console.log(status.responseText);
                Materialize.toast("Could not share on your timeline at this time", 4000);
                $("#preloadershare").css("display", "none");
            }
        });
    };

    //////////////// Mobile view (less than 992px) //////////////////
    //  Upload image from mobile view
    $("#upload-form-mobile").on("submit", function(event) {
        event.preventDefault();
        var fd = new FormData();
        var url = $(this).attr("action");
        var image = $(this).find("input[type='file']")[0].files[0];
        fd.append("image", image);
        mobile_upload_image(fd, url);
    });
    // AJAX for uploading image from mobile
    function mobile_upload_image(fd, url) {
        $(".preloader-mobile").css("display", "block");
        $.ajax({
            url: url,
            type: "POST",
            data: fd,
            contentType: false,
            processData: false,
            // On success
            success: function(json) {
                // Display the image in the center after upload
                var img_publicid = json.publicid;
                $("#img").attr("src", "http://res.cloudinary.com/myphotoapp/" + img_publicid);
                $("#upload-form-mobile #img-file").val("");
                $("#upload-form-mobile #img-file-path").val("");
                Materialize.toast("Upload Successful!", 4000);
                $(".preloader-mobile").css("display", "none");
                var img_src = $("#img").attr("src");
                $("#canvas").css("display", "block");
                $("#canvas").css("margin", "auto");
                filter(img_src);
            },
            error: function(status) {
                $("#upload-form-mobile #img-file").val("");
                $("#upload-form-mobile #img-file-path").val("");
                Materialize.toast("Invalid File Input!", 4000);
                $(".preloader-mobile").css("display", "none");
            }
        });
    };
});