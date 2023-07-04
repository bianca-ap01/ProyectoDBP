document.addEventListener('DOMContentLoaded', function() {
  var carousel = document.querySelector('.carousel');
  var flkty = new Flickity(carousel, {
    autoPlay: true,
    prevNextButtons: true,
    pageDots: true,
    wrapAround: true
  });
});