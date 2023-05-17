$(document).ready(function() {
  $('.faq-question').click(function() {
    var currentQuestion = $(this);
    var currentAnswer = currentQuestion.next('.faq-answer');

    $('.faq-answer').not(currentAnswer).slideUp('slow');
    currentAnswer.slideToggle('slow');

    if (currentQuestion.hasClass('expanded')) {
      currentQuestion.removeClass('expanded');
    } else {
      $('.faq-question').removeClass('expanded');
      currentQuestion.addClass('expanded');
    }
  });
});
