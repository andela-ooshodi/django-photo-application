function filter(img_src) {
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');

    /* Enable Cross Origin Image Editing */
    var img = new Image();
    img.crossOrigin = '';
    img.onload = function() {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0, img.width, img.height);
    }
    img.src = img_src;

    var $noise = $('#noisebtn');
    var $sepia = $('#sepiabtn');
    var $contrast = $('#contrastbtn');
    var $vintage = $('#vintagebtn');
    var $emboss = $('#embossbtn');
    var $orangepeel = $('#orangepeelbtn');
    var $sunrise = $('#sunrisebtn')
    var $oldpaper = $('#oldpaperbtn');
    var $save = $('#savebtn');

    /* Creating custom filters */
    Caman.Filter.register("oldpaper", function() {
        this.pinhole();
        this.noise(10);
        this.orangePeel();
        this.render();
    });

    /* In built filters */
    $noise.on('click', function(e) {
        $('#canvas').removeAttr('data-caman-id');
        Caman('#canvas', img, function() {
            this.noise(10).render();
        });
    });
    $contrast.on('click', function(e) {
        $('#canvas').removeAttr('data-caman-id');
        Caman('#canvas', img, function() {
            this.contrast(10).render();
        });
    });
    $sepia.on('click', function(e) {
        $('#canvas').removeAttr('data-caman-id');
        Caman('#canvas', img, function() {
            this.sepia(20).render();
        });
    });
    $vintage.on('click', function(e) {
        $('#canvas').removeAttr('data-caman-id');
        Caman('#canvas', img, function() {
            this.vintage().render();
        });
    });
    $emboss.on('click', function(e) {
        $('#canvas').removeAttr('data-caman-id');
        Caman('#canvas', img, function() {
            this.emboss().render();
        });
    });
    $orangepeel.on('click', function(e) {
        $('#canvas').removeAttr('data-caman-id');
        Caman('#canvas', img, function() {
            this.orangePeel().render();
        });
    });
    $sunrise.on('click', function(e) {
        $('#canvas').removeAttr('data-caman-id');
        Caman('#canvas', img, function() {
            this.sunrise().render();
        });
    });

    /* Applying Custom filters */
    $oldpaper.on('click', function(e) {
        $('#canvas').removeAttr('data-caman-id');
        Caman('#canvas', img, function() {
            this.oldpaper();
            this.render();
        });
    });

    /* You can also save it as a jpg image, extension need to be added later after saving image. */
    $save.on('click', function(e) {
        Caman('#canvas', img, function() {
            this.render(function() {
                this.save('png');
            });
        });
    });
};