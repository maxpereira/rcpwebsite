# Repair Café of the Peninsula website: how to update it

Static site served by GitHub Pages at repaircafepeninsula.org (see `CNAME`).
There is no build step: every page is a hand-written HTML file, and pushing to
`main` publishes it. **Work on a branch and push to `main` only when the owner
says to.**

The owner sends updates in two shapes. Each has a checklist below:

- **"New event: date X, signup URL Y"** → [A. Announce the next event](#a-announce-the-next-event)
- **"We had our event, here are the stats (and photos)"** → [B. Add a past event](#b-add-a-past-event)

---

## Site map

| Path | What it is |
|---|---|
| `index.html` | Home page |
| `volunteer/index.html` | Volunteer roles + sign-up |
| `past-events/index.html` | List of past events, newest first, with running totals |
| `past-events/YYYY-MM-<city>/index.html` | One recap page per event, e.g. `2026-10-san-carlos` |
| `eventsignup/index.html` | Short link `/eventsignup/` (used on flyers) that redirects to the current SignUpGenius page |
| `styles.css` | The only stylesheet, used by every page |
| `script.js` | Header border on scroll + mobile menu. FAQ uses native `<details>`, no JS |
| `fonts/` | Self-hosted Fraunces (headings) and Inter (body) |
| `images/events/YYYY-MM/` | Photos from that month's event |
| `images/photos/` | Photos whose event isn't known |
| `images/email.svg`, `email-light.svg` | The email address drawn as outlines (anti-scraping). Never write the address as plain text or `mailto:` |
| `tools/make_photos.py` | Turns an original photo into the web sizes (see [Photos](#photos)) |
| `sitemap.xml` | Every page with a `lastmod` date |

Every page repeats the same header and footer markup, adjusted for its depth:
`""` on the home page, `../` one level down, `../../` on recap pages. A change to
the nav or footer must be made on all five pages.

---

## Stats ledger

Keep this table current. The running totals on the site are computed from it.

| # | Date | Page | Visitors | Volunteers | Items | Fixed | Returned w/ instructions | Not fixed | Fix rate | Waste diverted |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-09-26 | `2026-09-san-carlos` | 28 | — | 38 | 25 | 8 | 5 | 66% | 112 lb 13 oz |
| 2 | 2026-10-24 | `2026-10-san-carlos` | 30 | 20 | 41 | 31 | 6 | 4 | 76% | 250 lb 7 oz |
| **Total** | | | | | **79** | **56** | **14** | **9** | **71%** | **363 lb 4 oz** |

- The owner's stats screenshot maps like this: Waste Diversion → waste, Unique People → Visitors,
  Unique Volunteers → Volunteers, Total Items → Items. Fixed, Not Fixed and Returned w/
  Instructions keep their names.
- Check that Fixed + Returned + Not fixed = Items. If not, ask before publishing.
- Fix rate = Fixed ÷ Items, rounded to a whole percent. Total fix rate = total Fixed ÷ total Items.
- Waste totals: add pounds and ounces separately and carry every 16 oz into a pound. Where the site
  shows whole pounds only (tallies, mini-tallies, meta descriptions), **drop the ounces**, don't
  round. So 112 lb 13 oz shows as 112 lb.
- Don't add up visitor or volunteer counts across events. People come back, so the sum would
  overcount.

---

## A. Announce the next event

Input: the date. Also a new SignUpGenius URL if there is one, and a time or place only if it changes
(the default is 3–6 PM at Callis & Elaine Community Center, 1336A Arroyo Ave, San Carlos, with
check-in closing at 5:30 PM).

Start with `grep -rn "<old date words>\|<old signup id>" --include=*.html .` to find every spot.
Then update:

**1. The next-event ticket.** There are five identical copies:
- `index.html` (`#next-event`)
- `volunteer/index.html` (`#next-event`)
- `past-events/index.html` (`#past-next`)
- every recap page (`#recap-next`)

In each copy update `ticket-dow` (Sat), `ticket-day` (21), `ticket-month` (Nov), `ticket-title`
("Saturday, November 21 · 3–6 PM") and the button `href`.

**2. The SignUpGenius URL, everywhere.**
- Replace the old URL on all pages.
- `eventsignup/index.html` has the URL **three** times: the meta refresh, the canonical link and
  the visible link.

**3. `index.html`**
- `meta description`, `og:description`, `twitter:description`: "Next event: Saturday, November 21, 2026, 3-6 PM in San Carlos…"
- JSON-LD `startDate` / `endDate`. Use `-07:00` while daylight saving is on (second Sunday of
  March to the first Sunday of November) and `-08:00` otherwise.
- The volunteer split button: "Sign up for Nov 21".
- FAQ "How often are events held?": "Our next event is Saturday, November 21st, 2026."

**4. `volunteer/index.html`**
- The three meta descriptions.
- Timeline step 1: "…you're on the schedule for November 21st."
- The closing section: "…for Saturday, November 21st…"

**5. `past-events/index.html`**
- The heading "Join us on November 21".

**6. If the time or place changed**, also update:
- `ticket-note` and the ticket's address and maps link (all five copies)
- the "3–6 PM" fact in `index.html`'s facts strip
- the FAQ "How often" answer and the JSON-LD `location`
- the hero sub-line ("…monthly repair event in San Carlos")

**7. Verify.**
- Grep again for the old date (e.g. "November 21", "Nov 21", `rcpnov`, `>21<`). There should be
  zero hits, except inside recap pages describing the past.
- Bump `sitemap.xml` `lastmod` for every page you changed.

---

## B. Add a past event

Input: the stats screenshot, ideally the event's Google Photos album link, and photos.

**1. Add the event's row to the [Stats ledger](#stats-ledger)** and recompute the totals.

**2. Photos.**
- Process them into `images/events/YYYY-MM/` (see [Photos](#photos)).
- Pick a landscape shot with a clear moment for the hero.

**3. Create the recap page.**
Copy the most recent recap to `past-events/YYYY-MM-<city>/index.html` (city in kebab-case,
e.g. `san-carlos`). Then change these, keeping the structure:

- `<title>` and `og:title` / `twitter:title`: `Repair Café of the Peninsula - <Month> <Year>, <City>`
- the three descriptions: `Results and photos from our <ordinal> Repair Café on <Month D, YYYY> in <City>: <Items> items, <Fixed> fixed, and over <lb> lb of waste diverted from landfill.`
- `og:url`
- **Hero:**
  - Swap the photo; it stays eager-loaded with `fetchpriority="high"`. For a portrait photo add
    `pos-top` to `<picture class="hero-photo">`.
  - Update the breadcrumb (`Past events › <Month> <Year>`), `hero-meta` (`Saturday, <Month D, YYYY> · 3–6 PM · <City>`)
    and the `<h1>` (`Our <ordinal> Repair Café`: first, second, third…).
- **Results:**
  - The `lead` is one factual sentence built from the stats. Compare with earlier events only
    when the numbers support it.
  - `headline-num`: `<lb><small>lb</small><oz><small>oz</small>`.
  - Outcome bar: always three segments, in the order Fixed, Returned, Not fixed. Set
    `style="flex: N;"` to the count. The Not fixed segment keeps the `is-light` class.
  - Each segment's `data-tip` reads `Fixed: 31 of 41 (76%)`, with each percent rounded. Update
    the bar's `aria-label`, the legend counts and the "What happened to the N items" title.
  - `stat-row`: Visitors, Volunteers (or Fixed when there's no volunteer count, as on the
    September page), Items, Fix rate. The row sizes itself to any number of items.
- **Photos:**
  - Set the album link (`View the full album`).
  - With 3 or more photos use `<ul class="photo-grid">`. The first photo is large; with exactly
    5 the fourth stretches on its own.
  - With 2 photos use `photo-grid photo-grid--pair`.
  - Every `<li>` gets `class="frame"`, and every image `loading="lazy" decoding="async"`.
- **Next event:** the ticket copy must match the other pages (section A, step 1).

**4. Update `past-events/index.html`.**
- Add a new `<li>` with an `event-row` at the **top** of `ol.event-list`, copied from the
  existing one. The photo side alternates automatically.
- Update the cover photo, `event-date`, `<h2>`, a one- or two-sentence summary, and the
  `mini-tally`: Items, Fixed, and whole pounds `Diverted`.
- Update the running `tally` at the top from the ledger totals.

**5. Update the running totals on `index.html`.**
- The `tally` in `#past-events`: items, fixed, fix rate, whole pounds.
- That section's kicker: "Two events in" → "Three events in".
- How-it-works step 3: "Of the 79 items brought to our first two events, 56 went home working."
- The volunteer split lead: "Twenty neighbors volunteered at our October event." Update it with
  the latest event's volunteer count and month, if given.
- Optionally swap fresher photos into the home page. Keep a photo in a single slot per page
  where possible.

**6. `sitemap.xml`**
- Add the new recap URL (`changefreq` yearly, priority 0.6).
- Bump `lastmod` on the changed pages.

**7. Next event.** If the owner gave the next date too, do section A.

---

## Photos

```
pip install pillow pillow-heif
python3 tools/make_photos.py <original> images/events/2026-11 <kebab-name>
```

- **Sizes:** the script writes WebP at 640/1024/1600/2400 (or up to the original's width) plus
  a 1024 JPEG fallback, and strips EXIF/GPS. Never commit an original straight off a phone.
- **Format:** iPhone `.heic` works. Photos pasted into the chat may not be saved to disk; ask for
  them as file attachments.
- **Markup:** use `<picture>` with a WebP `<source srcset="… 640w, … 1024w …" sizes="…">` and
  the JPEG `<img>` with `width`/`height` of that JPEG.
  - Below the fold: `loading="lazy" decoding="async"`.
  - The hero: `fetchpriority="high"`, and on the home page a matching `<link rel="preload" as="image">`.
- **Framing:** images that fill a fixed shape sit inside a `.frame` element. A portrait photo in
  a wide frame gets `pos-top` on the `<picture>` (or the frame) so heads stay in view.
- **Alt text:** describe what's happening ("A volunteer and a visitor opening up an espresso
  machine together"). Don't name people, even when name tags are visible. Don't call someone a
  volunteer unless that's known.

---

## Design and copy rules

These keep the site consistent. The redesign deliberately removed the "template" look.

- **Section structure:** `.section` (optionally `--deep` for the darker cream or `--dark` for
  green) → `.wrap` → a `.kicker` label → `<h2>`. Two-column sections use `.cols` (heading left,
  content right), with `.sticky` on the heading column if it's long.
- **No emoji icons, pill tags or card grids with hover lift.** Use `.kicker` for labels, ruled
  lists for collections, and the line SVG icon style from "What we fix" if an icon is needed.
- **Headings:**
  - Headings use Fraunces in green. One `<em>` per heading at most, for the clay-colored
    italic accent.
  - Numbers and stats use Inter semibold (`tally-num`, `headline-num`, `stat-row`,
    `mini-tally`), never the serif.
- **Colors:**
  - Use the CSS custom properties in `:root` and don't invent new hex values. Text colors
    were chosen for at least 4.5:1 contrast.
  - The outcome bar palette (`--outcome-*`) is a validated single-hue ramp; don't change it.
- **Inline styles:** no `style=""` attributes, except the outcome bar's `flex: N`. Add a small
  class in `styles.css` instead.
- **Cache-busting:** after changing `styles.css` or `script.js`, bump the `?v=YYYYMMDDx` query
  on every page's `<link>`/`<script>`.
- **Copy:**
  - Write "Repair Caf&eacute;" with the accent.
  - Use "Check-in closes at 5:30 PM".
  - Don't state how many items to bring anywhere except the FAQ, which says "up to two items
    per person per event".
  - Keep stats factual. Don't invent quotes, attendance or outcomes.

## Checking your work

```
python3 -m http.server 8765        # then open http://127.0.0.1:8765/
```

- **Pages and widths:** check every changed page at desktop (1440px) and phone (390px) widths.
  There should be no sideways scroll, and lazy images should appear as you scroll.
- **Stale text:** grep for the old date, the old signup id and the old totals.
- **Paths:** make sure every new image path exists. A typo in a `srcset` fails silently.

## Open items

- `images/photos/holiday-toy-*` and `images/photos/electronics-coach-*`: we don't know which
  event they're from. Once the owner says, move them to that month's folder and add them to that
  recap's photo grid.
