"use strict";

console.log("🔥 BACKGROUND.JS IS RUNNING");

/**
 * Receive messages from the content script.
 */
chrome.runtime.onMessage.addListener(
  (message, sender, sendResponse) => {
    // Only handle TEXT_SELECTED messages.
    if (message?.type !== "TEXT_SELECTED") {
      return;
    }

    const selectedText = message.data;

    console.log("Background received: ✅", selectedText);

    // Validate the selected text.
    if (
      typeof selectedText !== "string" ||
      !selectedText.trim()
    ) {
      sendResponse({
        ok: false,
        message: "Invalid selected text.",
      });

      return;
    }

    /**
     * Save the selected text into Chrome local storage.
     */
    chrome.storage.local.set(
      {
        selectedText: selectedText,
      },
      () => {
        // Check if storage operation failed.
        if (chrome.runtime.lastError) {
          console.error(
            "❌ Failed to save selected text:",
            chrome.runtime.lastError.message
          );

          sendResponse({
            ok: false,
            message: "Failed to save selected text.",
          });

          return;
        }

        console.log("✅ Selected text saved to chrome.storage.local");

        // Tell content.js that the text was successfully saved.
        sendResponse({
          ok: true,
          message: "Selected text saved successfully.",
        });
      }
    );

    // Important because sendResponse is called asynchronously.
    return true;
  }
);