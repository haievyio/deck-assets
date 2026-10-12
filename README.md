# Digicode deck assets (public)

Public images for Digicode presentations built with Gemini (the HTML Gem). Gemini Canvas can only show
images it can fetch from a public URL, so the deck slides link here, through jsDelivr:

    https://cdn.jsdelivr.net/gh/haievyio/deck-assets@v1/img/logo-white.svg

**Only images that are already public**: the Digicode logo, certification and partner badges,
illustrations, and mockups of approved cases that may be named (the same ones on mydigicode.com).
Never portraits, photos of employees, NDA or anonymised cases, client logos without the client's OK,
or Diger. Their frames use `img/photo-frame.svg`.

Google Drive is the source. Don't edit images here: change them in Drive, then run
`python3 scripts/publish.py <digicode-decks plugin path>`, commit, and tag a new version (`v2`, …).
`manifest.json` lists each image with its Drive id and checksum.

Temporary home under a personal account; it moves to `digicode-hq` later (the URLs will change then).
