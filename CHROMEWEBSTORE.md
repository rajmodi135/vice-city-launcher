# Chrome Web Store Listing: GTA Vice City Web Trainer Pro

This document maintains all listing metadata, store descriptions, permissions justifications, and privacy policy disclosures required for submitting the extension to the Chrome Web Store dashboard.

---

## 1. Store Listing Metadata

| Field | Content | Length/Limit |
|---|---|---|
| **Extension Name** | GTA Vice City Web Trainer Pro | Max 45 chars (30 used) |
| **Short Description** | Modern scrolling overlay trainer and keyboard shortcuts utility for browser play. | Max 150 chars (81 used) |
| **Category** | Developer Tools / Games / Fun | Category selection |
| **Language** | English (United States) | Default |

### Detailed Description (CWS Dashboard Rich Text)
```text
★ TAKE BACK CONTROL OF VICE CITY DIRECTLY IN YOUR BROWSER ★

Tired of typing long cheat codes manually and getting wasted while trying to trigger health or weapons? GTA Vice City Web Trainer Pro upgrades your online gameplay with a premium, arcade-style console overlay and hotkey manager.

Designed specifically for online emulator play, this extension injects a lightweight, borderless HUD directly on top of the game screen so you can activate cheats instantly.

FEATURES:
✔ Retro Arcade Overlay Menu: Press ` (Backtick) or F1 while gaming to open a transparent selection box on the left side of your screen. 
✔ Smart Scroll Viewport: Easily navigate the complete list of 18 cheats using your Up/Down Arrow keys. Glowing indicator lights alert you if more options exist.
✔ In-Browser Hotkeys: Avoid menus entirely! Tap Alt+Shift+[Key] (like Alt+Shift+H for health) to trigger cheats instantly in-game.
✔ Audio Feedback: Features a built-in Web Audio synthesizer that creates retro blip navigation sounds and chime execution alerts.
✔ Smart Tab Grabber: Click "LAUNCH GAME" from the toolbar popup and the extension will automatically find your open game tab—even if it is lost in a different window—and forcefully pull it into your current window for seamless access.
✔ Privacy First: Runs entirely locally in sandboxed environments. No data is stored, collected, or transmitted.

HOW TO USE IT:
1. Load the game in Chrome.
2. Tap ` (Backtick) or F1 to open the menu.
3. Select your cheat and hit Enter!
```

---

## 2. Permissions Justifications

These plain-English justifications are required by the Google extension review team:

| Permission | Technical Need | Plain-English Justification for Reviewers |
|---|---|---|
| **`tabs`** | Used to inspect URL match structures and activate/focus the game. | Required to detect if the game tab is already running in a background window and activate it. |
| **`scripting`** | Injecting event callbacks into the tab context. | Required to programmatically dispatch keypress events to simulate keyboard input inside the WebGL game canvas. |
| **`webNavigation`** | Querying all nested frames inside the active tab. | Required to find the frame ID of the cross-origin emulator iframe (vc.quenq.com) so cheats can be routed to the correct focus area. |

---

## 3. Privacy Policy & Data Disclosures

- **Data Collection**: The extension collects **Zero (0)** user data.
- **Data Transmission**: No data is transmitted to remote servers. All communications occur locally inside Chrome's memory space.
- **Data Storage**: No persistent local storage is utilized.
- **Privacy Policy URL**: (To be hosted on the developer's Github Pages or static site)
  ```text
  This privacy policy details that the "GTA Vice City Web Trainer Pro" Chrome Extension operates completely client-side. We do not collect, capture, transmit, or share any personal information, browsing history, or gameplay data. Keyboard events are generated purely inside your local browser page context to facilitate cheat triggering.
  ```

---

## 4. Release & Version History

- **v1.1.3** (2026-07-14)
  - Created a top-left floating helper note badge displaying controls on game load.
  - Implemented automatic fullscreen adaptive relocation for the helper note, and programmed it to fade out and delete itself on the first phone toggle.
- **v1.1.2** (2026-07-14)
  - Integrated "Powered by Mauxx AI" branding inside the phone interface and popup dashboard footer.
  - Added a toggleable 2D Grid Mode dashboard displaying app-style emojis for all cheats.
  - Built 2D Arrow Key navigation (Left, Right, Up, Down wrap-around coordinates) for grid selection.
- **v1.1.1** (2026-07-14)
  - Fixed gameplay GPU lag issues by removing expensive backdrop-filter blur parameters.
  - Implemented virtual smartphone `TAKE PHOTO` and `RECORD VIDEO` features using MediaStreams, generating automatic local PNG snapshots and WebM screen recording file downloads.
  - Added white flash screen transitions and synthesized camera shutter sound effects.
- **v1.1.0** (2026-07-14)
  - Removed all page-level keyboard cheat hotkeys (Alt+Shift combinations), focusing triggers solely on the smartphone overlay dialpad.
- **v1.0.9** (2026-07-14)
  - Mapped ArrowUp as phone opening hotkey when closed, and configured Backspace / Escape keys to close the phone.
- **v1.0.8** (2026-07-14)
  - Upgraded toggle listeners to inspect physical key codes (`e.code === "Backquote"` / `"F1"` / `"KeyP"`), resolving dead-key blockades on Linux platforms.
- **v1.0.7** (2026-07-14)
  - Restored smartphone layout to viewport fixed positioning, resolving layout blocks caused by zero-dimension or hidden-overflow canvas wrappers.
- **v1.0.6** (2026-07-14)
  - Broadened matches rules in manifest.json to wildcard subdomains (`*://*.quenq.com/*`) to capture sandboxed frame hosts.
  - Implemented dual capture-phase keydown listeners on both window and document to bypass emulator key capture blocks.
  - Added `Alt+Shift+P` global phone toggle fallback.
- **v1.0.5** (2026-07-14)
  - Added sandbox-safe frame loading detection using window tree hierarchy inspections (window !== window.top).
  - Integrated container layout protection checks (checking computed relative/absolute styles) to avoid shifting gameplay bounds.
- **v1.0.4** (2026-07-14)
  - Redesigned the virtual phone bezel casing to a light silver-blue theme with an oval speaker notch and home indicators mimicking the GTA V smartphone layout.
  - Relocated the overlay wrapper to sit directly inside the emulator canvas parent container, ensuring the smartphone sits directly on top of the WebGL canvas.
- **v1.0.3** (2026-07-14)
  - Added dynamic fullscreenchange event handlers inside the game frame to append/relocate the smartphone overlay directly inside active fullscreen DOM elements, preventing stacking context clipping.
- **v1.0.2** (2026-07-14)
  - Implemented canvas fullscreen request interception, redirecting fullscreen triggers to the canvas parent to keep the smartphone overlay visible during native fullscreen gameplay.
- **v1.0.1** (2026-07-14)
  - Upgraded overlay to a GTA V-style Virtual Smartphone HUD in the bottom-right.
  - Integrated real-time clock synchronization and status indicators inside the phone screen.
  - Added DTMF dial-tone telephone touch sound effects.
  - Implemented smooth spring slide-in/slide-out animations on phone open and close.
- **v1.0.0** (2026-07-14)
  - Production stable release.
  - Added Tekken scrolling overlay with arrow navigation.
  - Implemented Alt+Shift hotkeys.
  - Injected dynamic Web Audio sound effects.
  - Added tab migration window manager.
  - Added high-resolution neon icons.
