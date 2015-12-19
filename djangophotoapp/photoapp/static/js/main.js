// Make the input file empty
function empty_file_input() {
    $("#img-file").val("");
    $("#img-file-path").val("");
    $("#upload-form-mobile #img-file").val("");
    $("#upload-form-mobile #img-file-path").val("");
};

// hide upload button after file upload on large screens
function hide_upload_button() {
    $(".file-input").css("display", "block");
    $("#upload-button-lg").css("display", "none");
    $("#upload-form").css("margin-bottom", "50px");
};

// Activate modals after ajax load
function activate_modal() {
    empty_file_input();
    hide_upload_button();
    $(".modal-trigger").leanModal();
    $(".lean-overlay").each(function(){
        $(this).remove();
    });
};

var eventListeners = {
    init: function() {
        // Display the upload button after file has been attached
        $("#img-file").on("change", function() {
            $(".file-input").css("display", "none");
            $("#upload-button-lg").css("display", "block");
            $("#upload-form").css("margin-bottom", "20px");
        });
        // Focus the image to the center of page
        $("body").on("click", ".edit", function() {
            var img_id = $(this).attr("id").split("-")[1];
            var img_src = $("#img-" + img_id).attr("src")
            $("#img").attr("src", img_src);
            $("#img").attr("data-img-src", img_src);
            $("#img").attr("data-img-id", img_id);
            $("#img").css("display", "block");
            $(".single-view").css({"height": "auto", "max-height": "500px"});
        });
        // Reset the canvas with the current image
        $("#resetbtn").on("click", function(e) {
            var current_img = $("#img").attr("data-img-src");
            $("#img").attr("src", current_img);
        });
        // Share Image
        $("#sharebtn").on("click", function() {
            var img_src = $("#img").attr("src")
            facebook.share(img_src);
        });
        // Download Image
        $("#downloadbtn").on("click", function() {
            var img_src = $("#img").attr("src");
            $(this).attr("href", img_src);
        });
    }
};

var facebook = {
    init: function() {
        // Load FB JS SDK asynchronously
        $.getScript("//connect.facebook.net/en_US/sdk.js", function() {
            FB.init({
                appId: "1531263510520883",
                version: "v2.5"
            });
        });
    },
    share: function(img_src) {
        FB.ui({
            method: "feed",
            link: window.location.href,
            caption: "myPhotoApp",
            picture: img_src,
            description: "I just used myPhotoApp to edit this photo and I love it."
        }, function(response) {});
    }
};

var uploadForm = {
    init: function() {
        // Upload Image on submit
        $("body").on("submit", "#upload-form", function(event) {
            event.preventDefault();
            var fd = uploadForm.formContents($(this));
            var url = $(this).attr("action");
            uploadForm.uploadImage(fd, url);
        });
    },
    formContents: function(_this) {
        var fd = new FormData();
        var image = _this.find("input[type='file']")[0].files[0];
        fd.append("image", image);
        return fd;
    },
    uploadImage: function(fd, url) {
        $("#preloaderupload").css("display", "block");
        $.ajax({
            url: url,
            type: "POST",
            data: fd,
            contentType: false,
            processData: false,
            // On success
            success: function(json) {
                $("#preloaderupload").css("display", "none");
                Materialize.toast("Upload Successful!", 4000);
                $(".uploaded-images").load(document.URL + " .uploaded-images", activate_modal);
            },
            error: function(status) {
                $("#preloaderupload").css("display", "none");
                if (status.status == 405) {
                    Materialize.toast("Max upload allowed is 10MB!", 4000);
                } else {
                    Materialize.toast("Invalid File Input!", 4000);
                }
                empty_file_input();
                hide_upload_button();
            }
        });
    }
};

// Mobile view (less than 992px)
// Upload image from mobile view
var mobileUploadForm = {
    init: function() {
        $("body").on("submit", "#upload-form-mobile", function(event) {
            event.preventDefault();
            var fd = uploadForm.formContents($(this));
            var url = $(this).attr("action");
            mobileUploadForm.uploadImage(fd, url);
        });
    },
    uploadImage: function(fd, url) {
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
                $(".preloader-mobile").css("display", "none");
                var img_src = json.newest_image_src;
                var img_id = json.newest_image_id
                $("#img").attr("src", img_src);
                $("#img").attr("data-img-src", img_src);
                $("#img").attr("data-img-id", img_id);
                $("#img").css("display", "block");
                $(".single-view").css({"height": "auto", "max-height": "500px"});
                empty_file_input();
                Materialize.toast("Upload Successful!", 4000);
            },
            error: function(status) {
                $(".preloader-mobile").css("display", "none");
                empty_file_input();
                Materialize.toast("Invalid File Input!", 4000);
            }
        });
    }
};

// Delete Image
var deleteImage = {
    init: function() {
        $("body").on("click", ".delete-image", function() {
            var image_id = $(this).attr("id").split("-")[1];
            var url = "/home";
            deleteImage.del(image_id, url);
        });
    },
    del: function(image_id, url) {
        $.ajax({
            url: url,
            type: "DELETE",
            data: {
                image_id: image_id
            },
            success: function(json) {
                Materialize.toast("Delete Successful!", 4000);
                $(".uploaded-images").load(document.URL + " .uploaded-images", activate_modal)
            }
        });
    }
};

// Apply Filter
var applyFilter = {
    init: function() {
        $("body").on("click", ".filter", function() {
            var img_src = $("#img").attr("data-img-src");
            var img_id = $("#img").attr("data-img-id");
            var img_filter = $(this).attr("data-filter");
            var url = "/filter";
            applyFilter.filter(img_src, img_id, img_filter, url);
        });
    },
    filter: function(img_src, img_id, img_filter, url) {
        $.ajax({
            url: url,
            type: "GET",
            data: {
                img_src: img_src,
                img_id: img_id,
                img_filter: img_filter
            },
            success: function(json) {
                var img_src = json.filtered_img_path;
                $("#img").attr("src", img_src + "?" + new Date().getTime());
            },
            error: function(status) {
                console.log(status.responseText);
            }
        });
    }
};

$(document).ready(function() {
    // Triggers sidebar on mobile view
    $(".button-collapse").sideNav();
    // Triggers modal
    $(".modal-trigger").leanModal();
    eventListeners.init();
    facebook.init();
    uploadForm.init();
    mobileUploadForm.init();
    deleteImage.init();
    applyFilter.init();
});