chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "READ_PAGE") {
    // Selectors for common job sites
    const selectors = [
      ".jobs-description", // LinkedIn
      ".text-heading-large", // LinkedIn convention( About the job)
      "#jobDescriptionText", // Indeed
      ".description__text", // General
      '[class*="jobDescription"]', // Wildcard for many sites
      "main article", // Fallback
    ];

    let foundText = "";
    for (let s of selectors) {
      const el = document.querySelector(s);
      if (el && el.innerText.length > 100) {
        // Ensure it's actual content
        foundText = el.innerText;
        break;
      }
    }

    if (foundText) {
      // Send success back to the popup
      sendResponse({ success: true, data: foundText });
    } else {
      // Send error back to the popup
      sendResponse({ success: false, error: "Could not locate JD text." });
    }
  }
  return true; // Keeps the communication channel open for the async response
});
