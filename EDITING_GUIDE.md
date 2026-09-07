# Editing your academic website

This guide describes the actual files in this project. You can edit the site with a plain-text editor such as VS Code, or later with GitHub's file editor.

The small navigation theme button cycles **Auto → Light → Dark → Auto**. Auto follows the computer setting; Light and Dark override it. `public/theme.js` saves the selection in this browser's localStorage (`academic-site-theme`) and applies it across pages before rendering. It also follows live system changes in Auto and synchronises changes between tabs. If storage is unavailable the button still works for the current page. Dark CSS has separate selectors for an explicit theme and the no-JavaScript system fallback. Edit `.theme-toggle` in `custom.css` for button styling. Earlier descriptions of system-only selection below are superseded by this manual control.

Automatic light/dark appearance follows the visitor's operating-system/browser preference, including changes while the page is open. The last `prefers-color-scheme:dark` block in `custom.css` sets the dark background, text, links, buttons and scrolled navigation. The light theme retains white backgrounds and UV-blue text. Photographs and coloured social icons are unchanged; X becomes white in dark mode for visibility. Printing always uses the light scheme. No cookies, switch or JavaScript are needed for theme selection. The matching browser theme-colour metadata is in `build.py`.

CV now uses the IMT campus photo as a normal full-width header, with no blurred layer. Contact shows emails followed by the Spanish address in its left column and the uncropped UA hand-sculpture photo in its right column. Both assignments are editable in `content/images.json`: `cv` and `contact_photo`. On narrow screens the columns stack. Teaching still uses a blurred photo behind its fully visible blackboard image. Research uses `object-position:55% 43%` and a small leftward transform.

All page banners now share one compact height, defined by `--header-height` plus `--hero-content-height` in the final block of `custom.css`. Desktop content height is 180px, in addition to the navigation. The name, affiliations and labels occupy three rows on Home; its name and affiliation string are in `document('index', ...)` in `build.py`, without `<br>` tags. Narrow screens use larger shared heights to allow wrapping. The final shared sizing rules override the earlier per-page aspect ratios; changing those earlier ratios alone will not resize the banners.

The navigation now overlays each header photograph with white text and a subtle gradient. When it reaches the page content during scrolling, it becomes white with UV-blue text. Its CSS is the final “Navigation integrated into the photograph” block in `custom.css`; the small `public/header.js` script controls that scroll state and measures the navigation height. Without JavaScript, navigation still works as an overlay at the top, but does not remain fixed while scrolling. This script introduces no external requests or tracking.

Latest settings: the site background is white and the text uses UV blue, RGB(0,44,82), or `#002c52`. Photo overlays retain light text for contrast. Home has compact Publications, CV and Email buttons in `.profile-actions`. Its four topic tags are in the `topics` variable inside `document()` in `build.py`, below the institution subtitle. The commented line above the name remains separate. The welcome heading uses the full biography-column width; About me follows the italic introduction. Social icons have no added background, border radius or inner padding.

Contact now shows only the Spanish postal address, both emails, and all seven social icons. Coloured icon files are stored locally; X remains black. Teaching has no subtitle. Research again uses a full-width photo banner with overlaid text. In custom.css, .hero-research uses aspect-ratio:961/450 and .hero-image-research uses object-position:center 50%, framing the speaker and the top of the IMT lectern. The screen is intentionally retained. The original photograph is unchanged.

Coauthor links are stored in `content/coauthors.json` and applied automatically to matching abbreviated names in paper metadata. Edit that file to change a destination or add a new coauthor. Presentation notes automatically insert a single line break before “Previously known as”.

## 1. How it works

This is a **static website**. Visitors receive normal HTML pages, CSS stylesheets, photos and a PDF. There is no database, WordPress installation, subscription, login system or JavaScript framework to maintain.

Python is used only to generate the website. `build.py` reads the content files, assembles the shared header/footer and each page, copies the assets, and writes the complete website into `dist/`. Visitors do not need Python.

The workflow is:

```text
Edit build.py / content / CSS / public assets
                    ↓
              python build.py
                    ↓
       dist/ contains the resulting website
                    ↓
          Preview locally / GitHub Pages
```

Edit the source files described below, not the generated HTML in `dist/`: rebuilding replaces the generated pages.

## 2. File map

| File or folder | Purpose |
| --- | --- |
| `build.py` | Page layouts, navigation, headings, research-paper titles, teaching entries, contact details, CV links and shared footer |
| `content/inicio.json` | Original home-page paragraphs used in the biography |
| `content/research.json` | Original abstracts, presentation notes, conference list and seminar text |
| `content/images.json` | Assigns a photo to each page and the portrait |
| `content/socials.json` | All seven social/profile names, links and icon paths, in display order |
| `content/teaching.json`, `content/cv.json`, `content/contact.json` | Preserved migration reference text; these three files are not currently rendered directly |
| `styles.css` | Main site-wide layout, typography, colours and responsive rules |
| `custom.css` | Readable, commented overrides for the header, portrait, social grid and individual background crops; edit this first for visual changes |
| `public/assets/` | All photographs and the CV, including unused photographs for future use |
| `public/assets/icons/` | Local social icons |
| `dist/` | Generated website, including copies of every asset, used for preview and publication |
| `verify.py` | Checks internal destinations, migrated content and local assets |
| `.github/workflows/pages.yml` | Rebuilds and deploys to GitHub Pages when changes are pushed to `main` |

## 3. Preview changes on your computer

Open a terminal **inside the `site` folder**, then run:

```sh
python build.py
python verify.py
python -m http.server 8765 --bind 127.0.0.1 --directory dist
```

Open `http://127.0.0.1:8765/`. If the preview server is already running, only run the first two commands and refresh the page. Press Ctrl+F5 if your browser is showing an old cached stylesheet or image. To stop a server you started, press Ctrl+C in its terminal.

If Windows does not recognise `python`, try `py` instead. Python 3.10 or later is sufficient; the project uses only its standard library. The currently running preview was started using Codex's bundled Python.

You can also open `dist/index.html` directly, although embedded PDF behaviour depends on your browser.

## 4. Change the text on each page

### Home

Search in `build.py` for `home=blocks('inicio')`. The following `body=...` string contains the welcome heading, About me label, short introduction, left-column caption and buttons. Change the words between HTML tags; keep the tags and Python punctuation.

The three biography paragraphs come from **zero-based entries 3, 4 and 5** in `content/inicio.json`. Entries are objects surrounded by braces. Edit the `html` field; update the matching `text` field as well to keep the reference text consistent. The `html` field is what visitors see. The source arrays also contain original headings that are not automatically displayed.

For example:

```json
{
  "tag": "p",
  "text": "My updated biography.",
  "html": "My updated biography."
}
```

To add a fourth biography paragraph, add a similar object at the end of the JSON array and add its zero-based position to `[3,4,5]` in `build.py`. Avoid inserting it before existing entries unless you also update the numeric positions.

The large banner name and subtitle are in the `document('index', ...)` call immediately after the home layout. A `<br>` inserts a line break. The name in the top navigation is separate: search for `Juanfran Blázquiz Pulido` inside `document()`.

### Restore or replace the commented tagline

Search `build.py` for **`HOME_HERO_TAGLINE`**. The optional line is retained as an HTML comment:

```html
<!-- HOME_HERO_TAGLINE: <p class="eyebrow">ECONOMICS · BEHAVIOUR · DECISIONS</p> -->
```

It appears in the generated page source but is invisible to visitors. To show it, replace that quoted string with:

```html
<p class="eyebrow">YOUR NEW WORDS</p>
```

Keep the surrounding Python quotes and `if home else ...` expression intact.

### Research

In `build.py`, search for these section identifiers: `fields`, `publications`, `working-papers`, `work-in-progress`, `conferences`, `seminars`.

The `paper(...)` function produces one paper entry. Its arguments are:

```python
paper(title, metadata, presentation_note, abstract=None, link=None)
```

Titles, coauthors, journal/year, status labels and DOI/SSRN links are supplied in the `paper(...)` calls. Edit those strings directly. Abstracts and presentation notes are read from `content/research.json`:

| Zero-based entry | Used for |
| --- | --- |
| 6 | Published paper's presentation history and former title |
| 7 | Published paper's abstract |
| 10 | Working paper's presentation history |
| 11 | Working paper's abstract |
| 14 | Job-market paper's presentation history and former title |
| 16 | Strategic sophistication project's presentation history |
| 20–49 | Conference years and all 23 numbered entries |
| 51 | Seminars |

Edit the `html` field of these entries, keeping `text` consistent. For conferences, the generator also uses `text` to recognise years and numbers, so both fields matter. A year entry looks like `2026`; a conference entry starts with a number and a closing parenthesis, such as `23) ...`.

To add a paper, duplicate the appropriate `paper(...)` call within its section, replace its details and update the small section count (`01` or `04`) if appropriate. The optional abstract produces an expandable “Read abstract” panel.

To add conferences, also adjust the loop slice `b[20:50]` to include the new entries and update the seminar reference `b[51]` if its position moves. Keep conference numbers unique; presentation-note numbers link to `#conference-N`. `verify.py` currently checks the original 23 conferences: extend that check if you want it to require new entries too.

### Teaching

Search `build.py` for `courses=[`. Each course has six values in this order:

```python
('Undergraduate', 'Course title', 'Degree programme',
 'University of Alicante', 'Fall 2026', 'Spanish')
```

Edit a tuple to update a course. Add another tuple, separated by a comma, to add a course. Use `Graduate` or `Undergraduate` as the first value so the existing grouping recognises it. Courses appear in the order listed within each group.

### CV

Replace `public/assets/CV_Juanfran_Blazquiz.pdf` with your new PDF **using exactly the same filename** and rebuild. Both the embedded preview and download button update together.

If you use a different filename, search `build.py` for `CV_Juanfran_Blazquiz.pdf` and update every occurrence. Update the filename checked by `verify.py` as well. The CV page heading and explanatory sentence are in the `cv=...` block.

### Contact

Search `build.py` for `contact=...`. Edit the institution names, addresses and emails in that block. Each email appears in two places: its visible label and its `href="mailto:..."`. Change both so the button sends email to the correct address.

### Shared text

Navigation labels are in `pages=[...]` near the top of `build.py`. Keep `index` as the home filename even though the visible label is Home. The footer and header are in `document()`. Search for `Content last updated` when changing the footer date after an academic content update. Page titles and descriptions are also generated in `document()`.

## 5. Change the photos

The current assignments are in `content/images.json`:

```json
{
  "inicio": "assets/explanada-castillo.jpg",
  "research": "assets/research-defense.jpg",
  "teaching": "assets/pizarra.png",
  "cv": "assets/ua-mano.jpg",
  "contact": "assets/alicante-castillo.jpg",
  "portrait": "assets/BlazquizJ.jpg"
}
```

To choose another picture, copy it into `public/assets/`, then change the relevant path in this JSON file. Use forward slashes, preserve the filename's capitalisation and include the extension. The same portrait entry is used for the Home portrait, circular header photo and browser icon.

Unused images—including the IMT campus, Lucca and the other Alicante pictures—remain in `public/assets/`. The build copies them all into `dist/assets/`, so they will also be available on the server after publication. Unused photos are stored but are not loaded by visitors unless referenced. The original filenames and the shortened filenames used by the site are both retained where applicable.

### Adjust image position or zoom

Edit the commented background rules in `custom.css`. For example:

```css
.hero-image-research { object-position: center 59%; }
```

The vertical percentage selects which part of a photo stays visible when the banner crops it. Try a smaller or larger value, rebuild, and refresh. `object-fit: cover` fills the banner and crops excess image; `object-fit: contain` shows the whole image, potentially leaving space around it.

Teaching deliberately uses `contain`, with the image's original `1156/424` aspect ratio, to show the full hand and formulas present in the supplied file. Narrow screens may have extra background space. This cannot recover parts that were already outside the original photograph.

For overall banner height, override `.hero` or `.hero-home` in `custom.css`. Portrait, landscape and panoramic photos require different crops; changing the photo may warrant a new focal position.

## 6. Edit social profiles and icons

Open `content/socials.json`. Each object has `name`, `url` and `icon` fields. The order of these objects controls the order on the page: X, Bluesky, LinkedIn, Google Scholar, GitHub, ORCID, ResearchGate.

```json
{"name": "Bluesky", "url": "https://bsky.app/profile/juanfranbp4.bsky.social", "icon": "assets/icons/bluesky.svg"}
```

Change a URL or name directly. To replace an icon, put the new file in `public/assets/icons/` and update the path. Add or remove a complete object to add or remove a profile, taking care with commas. The home page uses small icons with names underneath, below the CV in the left column. The footer uses text links from the same data.

In `custom.css`, `.social-icons img` sets icon size, `.social-icons span` sets label size and `grid-template-columns` controls the number of columns. Decorative images use empty `alt` text because the visible name already labels each link.

## 7. Change fonts, colours and spacing

Prefer adding a clearly labelled rule to `custom.css`, which loads after `styles.css` and takes priority when selectors have the same specificity.

```css
/* Larger name in the top navigation */
.brand { font-size: 1.4rem; }

/* Link accent colour */
:root { --accent: #237666; }

/* Gap between the home photo column and biography */
.about-layout { gap: 64px; }
```

`styles.css` defines the main colours as variables: `--ink`, `--muted`, `--accent`, `--line` and `--navy`. Body text uses a system sans-serif font; headings use Georgia. There are no external font requests.

Rules inside `@media(max-width:720px)` apply to narrow screens. For example, the social grid uses four columns on most phones and three on very narrow phones. If you change desktop sizes, inspect the phone layout too. Keep text readable, leave keyboard focus outlines intact and preserve sufficient contrast over photos.

## 8. Publish edits through GitHub

Publication has not yet been completed. The organisation `juanfranblazquizpulido` has now been created, with `juanfranbp4` as its member/owner account. Once the repository and Pages setup are complete:

1. Open the website repository on GitHub.
2. Open the source file you want to edit and choose the pencil / Edit control.
3. Make the change, then choose Commit changes to save it to `main`.
4. The included GitHub Actions workflow runs `python build.py` and deploys `dist/`.
5. Check the Actions tab for a successful deployment, then refresh the public website.

Upload photos to `public/assets/`, not directly to `dist/assets/`. For several related changes, make them together before committing when possible. If a build fails, open its Actions log; a missing comma, unmatched quote or invalid JSON is a common cause.

The workflow requires Settings → Pages → Source to be set to GitHub Actions. A free organisation Pages website uses a public repository: its source and stored assets are publicly accessible.

## 9. Editing syntax and checks

JSON uses double quotes and commas between objects or fields, but no trailing comma after the last item. Inside JSON strings, escape double quotes as `\"`. Python strings also need matching quotes; when a title contains an apostrophe, surrounding it with double quotes can be clearer.

Useful HTML inside text strings: `<br>` for a line break, `<em>...</em>` for emphasis, `<strong>...</strong>` for bold and `<a href="URL">label</a>` for a link. In an f-string in `build.py`, `{...}` is a Python expression: leave it intact unless you mean to change the generator.

Run `python build.py` and `python verify.py` before publishing. Verification checks links, assets and selected migrated content; it is not a visual design test and does not guarantee that external websites remain available. GitHub records committed versions, so you can review history and restore earlier text if needed.



Advisor links on Home are in the html field of entry 3 in content/inicio.json. Teaching has a 6px downward CSS translation.

The theme control is now icon-only, with an accessible label and hover tooltip explaining the current and next modes. Social icons use two rows: X / Bluesky / LinkedIn, then Google Scholar / ORCID / ResearchGate / GitHub. The footer says “Find me online” and keeps links on one row on desktop, wrapping only on small screens. Adjust the final social/footer rules in custom.css.

