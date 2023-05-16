document.addEventListener("DOMContentLoaded", function () {
  const cards = document.querySelectorAll(".resource-card");

  cards.forEach(function (card) {
    card.addEventListener("mouseover", function () {
      cards.forEach(function (otherCard) {
        if (otherCard !== card) {
          otherCard.style.opacity = 0.6;
        }
      });
    });

    card.addEventListener("mouseout", function () {
      cards.forEach(function (otherCard) {
        otherCard.style.opacity = 1;
      });
    });
  });
});
