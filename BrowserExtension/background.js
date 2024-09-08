let lastResult = null;

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "sendMedia",
    title: "Detect Deepfakes",
    contexts: ["image", "video", "selection", "audio"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "sendMedia") {
    if (info.mediaType === 'image' || info.mediaType === 'video') {
      fetch(info.srcUrl)
        .then(response => response.blob())
        .then(blob => {
          const formData = new FormData();
          formData.append('file', blob, 'media');

          const endpoint = info.mediaType === 'video' ? 'http://127.0.0.1:5000/predict/video' : 'http://127.0.0.1:5000/predict';

          return fetch(endpoint, {
            method: 'POST',
            body: formData
          });
        })
        .then(response => response.json())
        .then(data => {
          console.log('Success:', data);
          lastResult = data;
          if (info.mediaType === 'video') {
            data = {
              predictions: data.map(pred => ({
                prediction: pred.prediction,
                probability: pred.probability
              }))
            };
          }
          chrome.tabs.create({ url: chrome.runtime.getURL('results.html') }, (newTab) => {
            chrome.tabs.onUpdated.addListener(function listener(tabId, changeInfo) {
              if (tabId === newTab.id && changeInfo.status === 'complete') {
                chrome.tabs.onUpdated.removeListener(listener);
                chrome.scripting.executeScript({
                  target: { tabId: newTab.id },
                  files: ['content.js']
                }, () => {
                  chrome.tabs.sendMessage(newTab.id, { type: 'RESULT', data: data });
                });
              }
            });
          });
        })
        .catch(error => console.error('Error:', error));
    } else if (info.selectionText) {
      fetch('http://localhost:8000/classify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: info.selectionText })
      })
        .then(response => response.json())
        .then(data => {
          console.log('Success:', data);
          // Transform the response format
          const transformedData = {
            predictions: [{
              prediction: data.result,
              probability: data.confidence
            }]
          };
          lastResult = transformedData;
          chrome.tabs.create({ url: chrome.runtime.getURL('results.html') }, (newTab) => {
            chrome.tabs.onUpdated.addListener(function listener(tabId, changeInfo) {
              if (tabId === newTab.id && changeInfo.status === 'complete') {
                chrome.tabs.onUpdated.removeListener(listener);
                chrome.scripting.executeScript({
                  target: { tabId: newTab.id },
                  files: ['content.js']
                }, () => {
                  chrome.tabs.sendMessage(newTab.id, { type: 'RESULT', data: transformedData });
                });
              }
            });
          });
        })
        .catch(error => console.error('Error:', error));
    } else if (info.mediaType === 'audio') {
      fetch(info.srcUrl)
        .then(response => response.blob())
        .then(blob => {
          const formData = new FormData();
          formData.append('audio_file', blob, 'audio');

          return fetch('http://127.0.0.1:8080/predict', {
            method: 'POST',
            body: formData
          });
        })
        .then(response => response.json())
        .then(data => {
          console.log('Success:', data);
          // Transform the response format
          const transformedData = {
            predictions: [{
              prediction: data.prediction,
              probability: data.confidence
            }]
          };
          lastResult = transformedData;
          chrome.tabs.create({ url: chrome.runtime.getURL('results.html') }, (newTab) => {
            chrome.tabs.onUpdated.addListener(function listener(tabId, changeInfo) {
              if (tabId === newTab.id && changeInfo.status === 'complete') {
                chrome.tabs.onUpdated.removeListener(listener);
                chrome.scripting.executeScript({
                  target: { tabId: newTab.id },
                  files: ['content.js']
                }, () => {
                  chrome.tabs.sendMessage(newTab.id, { type: 'RESULT', data: transformedData });
                });
              }
            });
          });
        })
        .catch(error => console.error('Error:', error));
    }
  }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'REQUEST_RESULT' && lastResult) {
    chrome.tabs.sendMessage(sender.tab.id, { type: 'RESULT', data: lastResult });
  }
});