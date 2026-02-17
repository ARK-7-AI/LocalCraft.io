document.getElementById('extractBtn').addEventListener('click', async () => {
  const statusDiv = document.getElementById('status');
  const RENDER_URL = "https://localcraft-io.onrender.com/submit-jd"; 

  statusDiv.style.display = 'block';
  statusDiv.className = 'info'; 
  statusDiv.innerText = "Searching for JD...";

  // 1. Find the active tab
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  // 2. Message to content.js
  chrome.tabs.sendMessage(tab.id, { action: "READ_PAGE" }, async (response) => {
    if (chrome.runtime.lastError) {
      showStatus("Error: Refresh the job page and try again.", "error");
      return;
    }

    if (response && response.success) {
      // --- START OF CLOUD BRIDGE LOGIC ---
      showStatus("Sending to Cloud...", "info");

      // Handle Render Cold Start UI
      const coldStartTimer = setTimeout(() => {
        showStatus("Waking up server (30-60s)... Please wait.", "warning");
      }, 2500);

      try {
        const apiResponse = await fetch(RENDER_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ jd: response.data })
        });

        clearTimeout(coldStartTimer);

        if (apiResponse.ok) {
          showStatus("Success! JD is in the queue.", "success");
          console.log("Cloud confirmed receipt.");
        } else {
          showStatus("Server Error: " + apiResponse.status, "error");
        }
      } catch (err) {
        clearTimeout(coldStartTimer);
        showStatus("Connection failed. Check your internet/API URL.", "error");
      }
      // --- END OF CLOUD BRIDGE LOGIC ---
      
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