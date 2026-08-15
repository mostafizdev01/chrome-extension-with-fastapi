"use strict";

console.log("🔥 POPUP.JS IS RUNNING");

// Get the selected-text element from popup.html
const selectedTextElement =
  document.getElementById("selected-text");

// Get the status element from popup.html
const statusElement =
  document.getElementById("status");

// Get the status indicator
const statusDot =
  document.querySelector(".status-dot");


/**
 * Display selected text inside the popup.
 */
function displaySelectedText(selectedText) {
  // Validate selected text
  if (
    typeof selectedText !== "string" ||
    !selectedText.trim()
  ) {
    return;
  }

  // Remove the placeholder
  selectedTextElement.innerHTML = "";

  // Create an element for the selected text
  const textElement = document.createElement("div");

  // Add the selected text safely
  textElement.textContent = selectedText;

  // Add text to the selected-text box
  selectedTextElement.appendChild(textElement);

  // Update status
  statusElement.textContent =
    "Text selected successfully.";

  // Update status indicator
  if (statusDot) {
    statusDot.style.background = "#22c55e";

    statusDot.style.boxShadow =
      "0 0 0 3px rgba(34, 197, 94, 0.12)";
  }
}


/**
 * Load the latest selected text from Chrome storage.
 */
function loadSelectedText() {
  chrome.storage.local.get(
    ["selectedText"],
    (result) => {

      // Check for storage errors
      if (chrome.runtime.lastError) {
        console.error(
          "❌ Failed to load selected text:",
          chrome.runtime.lastError.message
        );

        statusElement.textContent =
          "Failed to load selected text.";

        return;
      }

      // Check whether selected text exists
      if (
        typeof result.selectedText !== "string" ||
        !result.selectedText.trim()
      ) {
        console.log(
          "ℹ️ No selected text found in storage."
        );

        return;
      }

      console.log(
        "✅ Selected text loaded:",
        result.selectedText
      );

      // Display the saved text
      displaySelectedText(result.selectedText);
    }
  );
}


/**
 * Load saved text when the popup opens.
 */
loadSelectedText();