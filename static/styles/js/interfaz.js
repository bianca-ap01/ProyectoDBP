const textArray = ['Programación competitiva!', 'Pensamiento algorítmico!', 'Resolución de problemas!'];
let arrayIndex = 0;
let charIndex = 0;

function writeContent() {
  if(charIndex < textArray[arrayIndex].length) {
    document.getElementById("typed-text").textContent += textArray[arrayIndex].charAt(charIndex);
    charIndex++;
    setTimeout(writeContent, 50);
  } else {
    setTimeout(eraseContent, 500);
  }
}

function eraseContent() {
  if(charIndex > 0) {
    document.getElementById("typed-text").textContent = textArray[arrayIndex].substring(0, charIndex-1);
    charIndex--;
    setTimeout(eraseContent, 50);
  } else {
    arrayIndex++;
    if(arrayIndex>=textArray.length)
      arrayIndex=0;
    setTimeout(writeContent, 50);
  }
}
document.addEventListener('DOMContentLoaded', function() {
  if(textArray.length) setTimeout(writeContent, 200);
});