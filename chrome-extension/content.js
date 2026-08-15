"use strict";

/**
 * Detect the text selected by the user on a webpage.
 */
function handleTextSelection() {
  const selection = window.getSelection();

  const selectedText = selection
    ? selection.toString().trim()
    : "";

  // Ignore empty selections.
  if (!selectedText) {
    return;
  }

  // Send the selected text to the background service worker.
  chrome.runtime.sendMessage(
    {
      type: "TEXT_SELECTED",
      data: selectedText,
    },
    (response) => {
      // Avoid unchecked runtime errors if the background
      // service worker is unavailable.
      if (chrome.runtime.lastError) {
        console.warn(
          "Could not send selected text:",
          chrome.runtime.lastError.message
        );
        return;
      }

      if (response?.ok) {
        console.log("Selected text sent successfully.");
      }
    }
  );
}

/**
 * Detect text selection when the user releases the mouse button.
 */
document.addEventListener("mouseup", handleTextSelection);