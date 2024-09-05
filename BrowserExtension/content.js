chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'RESULT') {
    const resultsDiv = document.getElementById('results');
    const percentageText = document.getElementById('percentageText');
    if (resultsDiv && percentageText) {
      var prediction = message.data.predictions[0].prediction;
      var probability = parseInt(parseFloat(message.data.predictions[0].probability) * 100);
      if(prediction === "Fake"){
        document.getElementById('themeStylesheet').setAttribute('href', 'fakeresult.css');
      } else {
          document.getElementById('themeStylesheet').setAttribute('href', 'result.css');
      }
      resultsDiv.innerHTML = `<pre>${prediction}</pre>`;
      percentageText.innerHTML = `<pre>${probability}%</pre>`;
      updatePercentageCircle(parseInt(probability),prediction);
    }
  }
});

function updatePercentageCircle(percentage, prediction) {
  const circle = document.querySelector('.percentage-circle');
  const percentageText = document.querySelector('.percentage-text');

  let currentPercentage = 0;
  const increment = percentage > currentPercentage ? 1 : -1;
  const color = prediction === 'Fake' ? '#f44336' : '#4caf50';
  const animate = setInterval(() => {
      currentPercentage += increment;
      if ((increment > 0 && currentPercentage >= percentage) || (increment < 0 && currentPercentage <= percentage)) {
          clearInterval(animate);
          currentPercentage = percentage;
      }
      circle.style.background = `conic-gradient(${color} 0%, ${color} ${currentPercentage}%, #e0e0e0 ${currentPercentage}%, #e0e0e0 100%)`;
      percentageText.textContent = `${currentPercentage}%`;
  }, 10);
}
