$(document).ready(function() {
    $('.faq-question').click(function() {
        var currentAnswer = $(this).next('.faq-answer');
        $('.faq-answer').not(currentAnswer).slideUp('slow');
        currentAnswer.slideToggle('slow');
    });
});
