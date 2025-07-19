# QA Plan: LinkedIn Ratings Extension

## Steps to Load and Test the Extension in Chrome

1. **Build/Prepare the Extension Folder**
   - Ensure `manifest.json`, `contentScript.js`, `tooltip.css`, and icons are present in the `extension/` directory.

2. **Load the Extension in Chrome**
   - Open Chrome and go to `chrome://extensions/`.
   - Enable "Developer mode" (toggle in the top right).
   - Click "Load unpacked" and select the `extension/` folder.
   - Confirm the extension appears in the list.

3. **Navigate to LinkedIn**
   - Go to `https://www.linkedin.com/` and log in if required.
   - Visit a company page, e.g., `https://www.linkedin.com/company/google/`.

4. **Test Tooltip Functionality**
   - Hover your mouse over company links (usually in the header or about sections).
   - Observe if a tooltip appears near the cursor.
   - The tooltip should display "Loading ratings..." and then show ratings or an error message.

5. **Verify Tooltip Styling**
   - Tooltip should have a dark background, white text, rounded corners, and fade in/out smoothly.

6. **Test Multiple Companies**
   - Hover over links to different companies to ensure ratings are fetched and displayed for each.

7. **Check for Console Errors**
   - Open DevTools (F12) and check the Console for any errors or warnings related to the extension.

## Common Pitfalls & Troubleshooting

- **CORS Issues:**
  - If the tooltip says "Error fetching ratings.", your backend (FastAPI) must allow requests from `https://www.linkedin.com` (set CORS headers).

- **Backend Not Running:**
  - Ensure your FastAPI server is running and accessible at `http://localhost:8000/ratings`.

- **Selector Mismatch:**
  - If tooltips do not appear, LinkedIn may have changed their company link structure. Adjust the selector logic in `contentScript.js` (look for `/company/` in the link's href).

- **Tooltip Styling Not Applied:**
  - Make sure `tooltip.css` is loaded or styles are injected by the script. If not, add a `<style>` tag with the CSS in `contentScript.js`.

- **Multiple Tooltips:**
  - Only one tooltip should be visible at a time. If not, check for logic errors in tooltip creation/removal.

- **Not Working on All Pages:**
  - The extension only runs on URLs matching `https://www.linkedin.com/company/*`. Adjust `manifest.json` if you want broader coverage.

- **Network Issues:**
  - If running Docker, ensure ports are mapped and accessible from the browser.

## Notes on Selectors
- The script currently matches `<a>` elements with `/company/` in their `href`.
- If LinkedIn changes their DOM, update the selector logic in `contentScript.js` accordingly.
