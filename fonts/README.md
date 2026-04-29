Fonts for Hindi/Devanagari
-------------------------

This project uses Devanagari text. To ensure correct rendering and accurate string handling
in the website and backend, install or bundle a Devanagari font (recommended: Noto Sans Devanagari).

Options:
- Use Google Fonts in the frontend: add `<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari&display=swap" rel="stylesheet">` and apply in CSS.
- Or download `NotoSansDevanagari-Regular.ttf` and place it in this `fonts/` folder and serve it as a static asset.

Backend notes:
- The backend Python code uses UTF-8 and outputs JSON with `ensure_ascii=False` already; ensure the environment locale supports UTF-8.
- On servers without system Devanagari fonts, you can bundle the TTF and use it where rendering to images/PDFs is required.
