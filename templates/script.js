document.addEventListener('DOMContentLoaded', () => {
  const inputText = document.getElementById('inputText');
  const clearButton = document.getElementById('clearButton');
  const pasteButton = document.getElementById('pasteButton');
  const summarizeButton = document.getElementById('summarizeButton');
  const summary = document.getElementById('summary');
  const summaryLengthValue = document.getElementById('summaryLengthValue');
  const resultSection = document.querySelector('.result-section');
  const loadingIndicator = document.querySelector('.loading-indicator');
  const undoButton = document.getElementById('undoButton');
  const redoButton = document.getElementById('redoButton');

  let textHistory = [];
  let currentIndex = -1;

  // Function to update undo and redo buttons
  const updateButtons = () => {
      undoButton.disabled = currentIndex <= 0;
      redoButton.disabled = currentIndex >= textHistory.length - 1;
  };

  // Function to clear the input textarea
  clearButton.addEventListener('click', () => {
      inputText.value = '';
      textHistory.push('');
      currentIndex++;
      updateButtons();
  });

  // Function to paste text from clipboard
  pasteButton.addEventListener('click', async () => {
      try {
          const permission = await navigator.permissions.query({ name: 'clipboard-read' });
          if (permission.state === 'granted' || permission.state === 'prompt') {
              const clipboardData = await navigator.clipboard.readText();
              inputText.value += clipboardData;
              textHistory.push(inputText.value);
              currentIndex++;
              updateButtons();
          } else {
              console.error('Clipboard permission denied.');
          }
      } catch (error) {
          console.error('Error accessing clipboard:', error);
      }
  });

  // Function to undo text changes
  undoButton.addEventListener('click', () => {
      if (currentIndex > 0) {
          currentIndex--;
          inputText.value = textHistory[currentIndex];
          updateButtons();
      }
  });

  // Function to redo text changes
  redoButton.addEventListener('click', () => {
      if (currentIndex < textHistory.length - 1) {
          currentIndex++;
          inputText.value = textHistory[currentIndex];
          updateButtons();
      }
  });

  // Function to summarize text
  summarizeButton.addEventListener('click', () => {
      const text = inputText.value.trim();
      if (!text) {
          summary.textContent = 'Please enter text to summarize.';
          return;
      }

      const summaryLength = parseInt(summaryLengthValue.value);
      loadingIndicator.removeAttribute('hidden');
      resultSection.setAttribute('hidden', true);

      // Simulate sending text and length to a backend (replace with API call if needed)
      setTimeout(() => {
          const summaryText = `This is a placeholder summary generated based on a requested length of ${summaryLength} percent.`;
          summary.textContent = summaryText;
          loadingIndicator.setAttribute('hidden', true);
          resultSection.removeAttribute('hidden');
      }, 2000); // Simulated delay of 2 seconds
  });
   // Function to save summarized text to clipboard
   saveButton.addEventListener('click', () => {
    const textToCopy = summary.textContent;
    navigator.clipboard.writeText(textToCopy)
        .then(() => {
            alert('Summary copied to clipboard!');
        })
        .catch(err => {
            console.error('Error copying text to clipboard:', err);
            alert('Failed to copy summary to clipboard. Please try again.');
        });
});
});
