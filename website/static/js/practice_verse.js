let originalVerseText = '';

// Store original verse text when page loads
function storeOriginalVerseText() {
    const verseText = document.getElementById('verse-text');
    if (verseText) {
        originalVerseText = verseText.textContent.trim();
    }
}

// Add to DOMContentLoaded event
document.addEventListener('DOMContentLoaded', function () {
    storeOriginalVerseText();
});

function matchTextareaSize() {
    const textarea = document.getElementById('answer');
    const verseText = document.getElementById('verse-text');
    const illusionWord = document.getElementById('illusion-word');
    // Check if text is more than 3 rows

    if (textarea && illusionWord) {
        // Copy text content
        illusionWord.textContent = textarea.value;
        const originalText = originalVerseText;
        console.log(originalText);
        verseText.textContent = textarea.value + originalText.substring(textarea.value.length);


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

        // Focus the textarea
        textarea.focus();
    }
});

// Add function to focus textarea
function focusTextarea() {
    const textarea = document.getElementById('answer');
    if (textarea) {
        textarea.focus();

        textarea.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                const form = textarea.closest('form');
                if (form) {
                    form.submit();
                }
            }
        });
    }
}

// Add event listeners for common user interactions
document.addEventListener('click', focusTextarea);
document.addEventListener('keydown', focusTextarea);

