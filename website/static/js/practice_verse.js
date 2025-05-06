// function getCurrentWordCoordinates(text, cursorPosition) {
//     const beforeSpace = text.lastIndexOf(" ", cursorPosition);
//     const afterSpace = text.indexOf(" ", cursorPosition);
//     const start = beforeSpace === -1 ? 0 : beforeSpace + 1;
//     const end = afterSpace === -1 ? text.length : afterSpace;
//     const currentWord = text.substring(start, end);
//     return [start, end];
// }

// function updateHighlightedWord() {
//     const textarea = document.getElementById('answer');
//     const highlightedWordDiv = document.getElementById('highlighted-word');

//     // Get cursor position and coords
//     const cursorPosition = textarea.selectionStart;
//     const currentWordCoordinates = getCurrentWordCoordinates(textarea.value, cursorPosition);
//     if (currentWordCoordinates[1] - currentWordCoordinates[0] > 0) {
//         const textareaWidth = textarea.offsetWidth;
//         const sumSpaceCharPixels = (textarea.value.split(' ').length - 1) * 6;
//         const matches = textarea.value.match(/[a-zA-Z0-9]/g);
//         const alphaNumericCount = matches ? matches.length : 0;
//         const sumAlphaCharPixels = alphaNumericCount * 8;
//         const charsPerLine = Math.floor((textareaWidth - 24) / 8); // 24px padding, ~8px per char

//         const textBeforeWord = textarea.value.substring(0, currentWordCoordinates[0]);

//         let wordStart = textBeforeWord.length;
//         let lineNumber = 0;
//         let wordStartNormalized = wordStart;
//         const lineHeight = 20; // Approximate line height in pixels
//         if (wordStart > charsPerLine) {
//             let lineNumber = Math.floor(wordStart / charsPerLine);
//             wordStartNormalized = wordStart - (lineNumber * charsPerLine)
//         }
//         // Position the highlighted word div
//         const formFontSize = window.getComputedStyle(textarea).fontSize;
//         highlightedWordDiv.style.fontSize = formFontSize;
//         highlightedWordDiv.textContent = textarea.value.substring(currentWordCoordinates[0], currentWordCoordinates[1]);
//         highlightedWordDiv.style.display = 'block';
//         highlightedWordDiv.style.color = 'red';
//         highlightedWordDiv.style.top = ((lineNumber * lineHeight) + 17) + 'px';
//         highlightedWordDiv.style.left = (((wordStartNormalized) * 8) + 17) + 'px';
//         console.log("Left: ", highlightedWordDiv.style.left, "Top: ", highlightedWordDiv.style.top)
//     } else {
//         highlightedWordDiv.style.display = 'none';
//     }
// }

// // Initialize the practice verse functionality
// document.addEventListener('DOMContentLoaded', function () {
//     const answerTextarea = document.getElementById('answer');
//     const submitButton = document.getElementById('submit-verse');

//     if (answerTextarea) {
//         answerTextarea.focus();

//         // Add event listeners for input and cursor movement
//         answerTextarea.addEventListener('input', updateHighlightedWord);
//         answerTextarea.addEventListener('keyup', updateHighlightedWord);
//         answerTextarea.addEventListener('click', updateHighlightedWord);

//         // Handle Enter key press
//         answerTextarea.addEventListener('keypress', function (event) {
//             if (event.key === 'Enter') {
//                 event.preventDefault();
//                 if (submitButton) {
//                     submitButton.click();
//                 }
//             }
//         });
//     }
// });


function matchTextareaSize() {
    const textarea = document.getElementById('answer');
    const illusionWord = document.getElementById('illusion-word');
    if (textarea && illusionWord) {
        // Copy text content
        illusionWord.textContent = textarea.value;

        // Match size and position
        const textareaStyle = window.getComputedStyle(textarea);
        illusionWord.style.width = textareaStyle.width;
        illusionWord.style.height = textareaStyle.height;
        illusionWord.style.fontSize = textareaStyle.fontSize;
        illusionWord.style.lineHeight = textareaStyle.lineHeight;
        illusionWord.style.padding = textareaStyle.padding;
        illusionWord.style.fontFamily = textareaStyle.fontFamily;
        illusionWord.style.whiteSpace = 'pre-wrap';
        illusionWord.style.color = 'red';

        // Position absolutely over textarea
        const textareaRect = textarea.getBoundingClientRect();
        illusionWord.style.position = 'absolute';
        illusionWord.style.top = `0px`;
        illusionWord.style.left = `0px`;
        illusionWord.style.width = `${textareaRect.width}px`;
        illusionWord.style.height = `${textareaRect.height}px`;
        console.log("value: ", illusionWord.textContent);
    }
}

// Add event listeners to keep sizes synced
document.addEventListener('DOMContentLoaded', function () {
    const textarea = document.getElementById('answer');
    if (textarea) {
        textarea.addEventListener('input', matchTextareaSize);
        textarea.addEventListener('keyup', matchTextareaSize);
        window.addEventListener('resize', matchTextareaSize);

        // Initial size match
        matchTextareaSize();
    }
});

