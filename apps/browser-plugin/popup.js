document.getElementById('extractBtn').addEventListener('click', async () => {
  const statusDiv = document.getElementById('status');
  statusDiv.style.display = 'block';
  statusDiv.className = ''; 
  statusDiv.innerText = "Searching for JD...";

  // 1. Find the active tab
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  // 2. Inject/SendMessage to content.js
  chrome.tabs.sendMessage(tab.id, { action: "READ_PAGE" }, (response) => {
    // Check if content script is even there
    if (chrome.runtime.lastError) {
      showStatus("Error: Navigate to a job post and refresh.", "error");
      return;
    }

    // Check the response from content.js
    if (response && response.success) {
      showStatus("JD Extracted Successfully!", "success");
      console.log("Extracted Data:", response.data); 
    } else {
      showStatus(response?.error || "Error: No JD found on page.", "error");
    }
  });
});

function showStatus(text, type) {
  const statusDiv = document.getElementById('status');
  statusDiv.innerText = text;
  statusDiv.className = type;
}