chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'RESULT') {
    const resultsDiv = document.getElementById('results');
    if (resultsDiv) {
      resultsDiv.innerHTML = `<pre>${JSON.stringify(message.data, null, 2)}</pre>`;
    }
  }
});