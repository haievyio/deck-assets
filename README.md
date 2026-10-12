# Digicode deck assets (public)

Public images for Digicode presentations built with Gemini (the HTML Gem). Gemini Canvas can only show
images it can fetch from a public URL, so the deck slides link here, through GitHub Pages
(jsDelivr refuses repos over 50 MB):

    https://haievyio.github.io/deck-assets/img/logo-white.svg

**All deck images** (decided 2026-10-12): logos, badges, icons, illustrations (deck set and SVG
library), office photos, leadership portraits and case mockups. Never Diger, and never NDA or
anonymised cases (their screens can show the client's name). Their frames use `img/photo-frame.svg`.

Google Drive is the source. Don't edit images here: change them in Drive, then run
`python3 scripts/publish.py <digicode-decks plugin path>`, commit, and tag a new version (`v2`, …).
`manifest.json` lists each image with its Drive id and checksum.

Temporary home under a personal account; it moves to `digicode-hq` later (the URLs will change then).
