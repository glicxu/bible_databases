# Bible PWA Project Plan

This document outlines the development plan for the Bible PWA, breaking down features into phased releases.

**Architecture:**
- **Backend:** Python Server (e.g., Flask, FastAPI)
- **Frontend:** Progressive Web App (PWA) (e.g., using a modern JavaScript framework like Vue, React, or Svelte, or vanilla JS)

---

## Phase 1: Minimum Viable Product (MVP)

**Goal:** Launch a functional, core reading application that users can install on their devices and use for basic Bible study.

### Backend (Python)
- [ ] **Setup Basic Server:** Initialize a Python web server project.
- [ ] **API - List Translations:** Create an endpoint (`/translations`) to serve the list of available Bible translations from the `translations` table/JSON.
- [ ] **API - List Books:** Create an endpoint (`/translations/{translation_abbr}/books`) to list the books for a specific translation.
- [ ] **API - Get Chapter:** Create an endpoint (`/translations/{translation_abbr}/{book_id}/{chapter}`) to serve the text for a full chapter.

### Frontend (PWA)
- [ ] **Basic PWA Setup:**
    - [ ] Create `manifest.json` for "Add to Home Screen" functionality.
    - [ ] Implement a basic Service Worker for app shell caching.
- [ ] **UI - Navigation:**
    - [ ] Home screen to select a Bible translation.
    - [ ] View to select a book and chapter.
- [ ] **UI - Reader View:**
    - [ ] Display the full text of a selected chapter.
    - [ ] Simple navigation to the next/previous chapter.
- [ ] **Offline Access (Basic):**
    - [ ] Cache recently read chapters for offline viewing.

---

## Phase 2: Enhanced Study & User Experience

**Goal:** Add key study tools and user experience improvements that make the app more powerful and comfortable to use.

### Backend (Python)
- [ ] **API - Search:** Create a robust search endpoint (`/search?q={query}&translation={translation_abbr}`) to find verses containing specific text.
    - [ ] *Consider: Pre-building a search index (e.g., using Whoosh or Bleve) for performance.*
- [ ] **API - Cross-References:** Create an endpoint (`/cross-references/{book}/{chapter}/{verse}`) to serve related verses from the cross-reference data.

### Frontend (PWA)
- [ ] **Feature - Parallel View:**
    - [ ] Implement a side-by-side reader view to compare the same chapter across two or more translations.
- [ ] **Feature - Search:**
    - [ ] Implement a search bar and a results page.
- [ ] **Feature - Interactive Text:**
    - [ ] **Dictionary Lookup:** Allow users to tap a single word to see a quick definition.
        - [ ] *Note: Requires integrating a dictionary API or dataset.*
    - [ ] **Text Selection Menu:** When a user selects one or more words, show a context menu with options:
        - [ ] Copy selected text.
        - [ ] Search for selection within the Bible.
        - [ ] Look up cross-references for the verse(s) in the selection.
- [ ] **Feature - Translation Switching:**
    - [ ] Add a dropdown/menu in the reader view to quickly switch the current chapter to a different translation.
- [ ] **UX - Display Customization:**
    - [ ] Implement controls for font size adjustment.
    - [ ] Add a theme switcher for Light and Dark modes.
- [ ] **Offline Access (Advanced):**
    - [ ] Implement functionality for users to download one or more full translations for complete offline reading.

---

## Phase 3: Personalization & Engagement

**Goal:** Implement features that allow users to personalize their study experience and engage with the content more deeply. This phase likely requires user accounts.

### Backend (Python)
- [ ] **User Accounts:**
    - [ ] Implement user registration and authentication (e.g., using JWTs).
- [ ] **API - User Data:** Create authenticated endpoints to save and retrieve:
    - [ ] Bookmarks
    - [ ] Highlighted verses
    - [ ] Personal notes attached to verses
- [ ] **API - AI/ML Features (Advanced):**
    - [ ] Create an endpoint to process a text selection and return a summary.
        - [ ] *Note: Requires an external AI service (e.g., OpenAI, Gemini) or a self-hosted model.*
- [ ] **API - Reading Plans:** Create endpoints to serve pre-defined reading plans.
- [ ] **API - Verse of the Day:** Create an endpoint to serve a daily verse.

### Frontend (PWA)
- [ ] **Feature - User Accounts:** Implement login and registration forms.
- [ ] **Feature - Highlighting & Notes:** Integrate with the text selection menu to allow users to highlight verses or attach personal notes to their account.
- [ ] **Feature - Bookmarking:** Allow users to bookmark their current reading location.
- [ ] **Feature - Reading Plans:** Display reading plans and allow users to track their progress.
- [ ] **Feature - AI Summary:** Integrate with the text selection menu to offer a "Summarize" option.
- [ ] **UI - Dashboard:** Create a user dashboard to show the "Verse of the Day", continue reading, and progress in reading plans.