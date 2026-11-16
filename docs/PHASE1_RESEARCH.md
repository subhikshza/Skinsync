# SkinSync — Phase 1 Research

_Last updated: 16 Nov 2026. Research from Phase 1, updated in Phase 2 to match the built rules and the new problem statement._

**How to read the "verified" labels**

- **Verified** = I read it on the tool's own page (support doc, official site, or app store listing).
- **Claimed** = the tool's own marketing says it, but I found no detail on how it works.
- **Unverified** = I found no evidence either way, or only a third-party blog. Do not state these as facts in an interview.

I did not install or use any of these apps. Everything below comes from public pages. Check an app yourself before you say "X can't do Y" to an interviewer.

---

## Step 1: Competitor research

### The five you named

| Tool | What it does | Checks conflicts BETWEEN products? | Builds routines? | Indian brand coverage | Pricing | Gaps |
|---|---|---|---|---|---|---|
| **INCIDecoder** | Explains each ingredient in a product in plain English. Can decode a pasted or photographed ingredient list. [About page][i1] | **Unverified.** No source I found mentions it. | **Unverified.** No source I found mentions it. | Unverified. Products are user-uploaded and checked by their team. [About page][i1] | Unverified (looks free) | One product at a time. It teaches, it does not plan. |
| **SkinSort** | Ingredient checker, product compare, dupe finder, shelves, routine creator. [Routine Creator doc][s1] | **Claimed.** Their marketing page says you get warnings when products don't mix well. [SkinSort vs SkinCarisma][s3] Their support docs do not describe it. Premium "Ingredient Warnings" and "Routine Insights" are about your skin profile, not product pairs. [Routine Insights doc][s2] | **Verified, manual.** You add products yourself, split AM/PM, pick days of the week. **It does not auto-generate a routine**; that is listed as a future idea. [Routine Creator doc][s1] | **Partly verified.** Indian products exist through user submissions (Dot & Key, Simple India, Vaseline India). [Example][s5] [Example routine][s6] Depth is unverified. | Free core. Premium about $7.99/month or $39.99/year on the US App Store. [App Store][s4] | You schedule the week yourself. Best insights are paid. App is iOS only (web works anywhere). |
| **CosDNA** | Rates each ingredient: acne 0 to 5, irritation 0 to 5, safety 1 to 10. [CosDNA help][c1] | **Unverified.** No evidence found. | **Unverified.** No evidence found. | Unverified (user-submitted database). | Unverified (looks free) | Scores per ingredient only. No "how do I use these together". |
| **Yuka** | Scan a barcode, get a 0 to 100 health score with a colour code. Cosmetics are scored on ingredient health risk. [Yuka app page][y1] | **No evidence.** Its feature page lists nothing about combining products. [Yuka app page][y1] | **No evidence.** Same page. | **Verified: not available in India.** India is not in Yuka's official country list. [Yuka help][y2] | Free. Premium adds search and offline mode. [Yuka app page][y1] About EUR 10/year per a third-party report. [Food Times][y3] | Not in India. Scores safety, not compatibility. |
| **Skin Bliss** | Face scan, product scanner, compatibility checker, routine builder, tracking. [App Store][b1] | **Verified (listing).** Has an Ingredient Compatibility Checker for clashes between products in a routine. [App Store][b1] | **Verified (listing).** Routine builder with scheduling, daily or on rotation. [App Store][b1] How automatic it is: unverified. | Unverified. Claims 100k+ products. [App Store][b1] | Free download. Pro about $6.99/month or $34.99/year. Which routine tools are paid: unverified. [App Store][b1] | Subscription. Not India-focused. Does not show its rule sources (unverified). |

### Others I found (these matter more than the big names)

| Tool | What it does | Conflicts between products? | Builds routines? | Indian brands | Pricing | Gaps |
|---|---|---|---|---|---|---|
| **Skincare Routine (Mento Apps)** | Routine organiser. **Closest paid app to SkinSync.** [App Store][m1] | **Verified (listing).** Warns about products that should not be used together. | **Verified (listing).** Auto-orders AM/PM in layering order. Day-of-week scheduling. | **Verified weak.** Preloaded with DECIEM brands only (The Ordinary, NIOD). Everything else is manual entry. | One-off about $5.99 | iOS app. No Indian catalogue. You still pick the days. |
| **SkinGuard** | Scanner plus AM/PM builder with a conflict engine. [App Store][g1] | **Claimed (listing).** Lists Retinol + AHA and Vitamin C + Niacinamide as conflicts. | **Claimed (listing).** Drag-and-drop AM/PM. | Unverified | Unverified | Treats Vitamin C + Niacinamide as a conflict, which cosmetic chemists call a myth (see rules table). |
| **SkinCare IQ** (student project, GitHub Pages) | Rule engine plus Gemini. **Closest project to SkinSync in concept.** [Site][iq] | **Claimed.** Local rule engine with journal-cited rules. | **Claimed.** Splits high-severity conflicts across alternate nights. | Unverified | Free | Limited to 2 to 4 products per analysis per its own UI. Not India-focused. |
| **GlamGuider** (India) | Ingredient explanations, acne-trigger flags, reviews, routines by skin type. [Listing summary][gg] | Not mentioned in listing | Yes, by skin type and concern | Calls itself India's ingredient-first platform. Brands unverified. | Free download | Under 1,000 downloads per the listing. No conflict check mentioned. |
| **SkinBB Label Looker** (India) | AI ingredient scanner on a 1,000+ ingredient database. [Press release][sb] | Not mentioned | Not yet. Planned for version 2.0. | Indian platform | Unverified | Explains ingredients only. |
| **LoveSkin** (India, Atavika) | AI routine builder using compatible ingredients. [Blog][ls] | Implied, no dedicated checker described | Yes, AM and night | Says Indian and international brands | Unverified | **Not launched** as of that blog post. |
| **The Derma Co app** (India) | Brand store that builds a routine. [Brand blog][dc] | Unverified | Claimed by the brand | Own products | Free | A storefront. It will recommend its own products. |

### What the research says (be honest about this)

1. **Conflict checking between products already exists.** Skin Bliss, Mento's Skincare Routine, SkinGuard and SkinCare IQ all do some form of it. You cannot say "no tool checks conflicts".
2. **AM/PM routine building also exists.** SkinSort, Skin Bliss and Mento all have it.
3. **The real gaps are narrower:**
   - **G1. Manual scheduling.** The biggest tool, SkinSort, makes you place every product on every day yourself. [Doc][s1]
   - **G2. India.** Yuka is not in India. [Help][y2] Mento preloads only DECIEM brands. [Listing][m1] SkinSort has Indian products only where users submitted them. The Indian apps I found either explain ingredients (SkinBB), sell their own range (Derma Co), or are unlaunched or tiny (LoveSkin, GlamGuider).
   - **G3. No visible sources.** I did not find a mainstream app that shows the source behind each warning (unverified for apps I could not open). At least one app lists a myth as a conflict. [SkinGuard][g1]
   - **G4. Paywalls.** The deeper routine features sit behind $7 to $8 a month subscriptions. [SkinSort][s4] [Skin Bliss][b1]
   - **G5. Beginners get warnings, not a plan.** A flag saying "retinol and AHA conflict" does not tell a beginner which nights to use each. (Unverified for apps I could not open.)

---

## Step 2: Problem statement

> Indian students who are new to skincare actives buy several products and do not know which ones clash or how to space them across the week.
> Other tools explain ingredients or flag a clash; SkinSync builds the whole AM/PM week for you from products sold in India, and shows the source behind every rule.

The three differences in line 2: it plans (not only warns), it is built for the Indian shelf, and its rules are sourced.

---

## Step 3: What's new

Nothing here is a world-first. Each point is pitched as "better for X".

### v1 (about 14 hours of work: 2 weeks at 1 hour a day)

| # | Differentiator | Gap | Honest status | How to pitch it |
|---|---|---|---|---|
| D1 | **Auto-scheduled week.** Pick your products, get a 7-day AM/PM grid. No dragging. | G1, G5 | Exists in parts elsewhere (Mento auto-orders AM/PM; SkinCare IQ alternates nights). SkinSort does not auto-generate. | "Better for beginners: you get a plan, not a list of warnings." |
| D2 | **Every rule shows its source and its reason** (irritation vs deactivation vs myth). | G3 | SkinCare IQ also claims cited rules. Mainstream apps: not found. | "Better for trust: you can click through and check me." |
| D3 | **India-first catalogue.** Products sold in India, prices in rupees. | G2 | v1 has 30 hand-entered products, 25 of them from Indian brands. That is small. Say so. | "Better for an Indian student's actual shelf." |
| D4 | **Beginner-safe frequency.** Retinoids start on alternate nights. Wash-off acids are treated as milder than leave-on acids. | G5 | Standard dermatology advice. The value is building it into the schedule. | "Better for first-time users of actives." |
| D5 | **Free, no login, runs in a browser.** | G4 | Plenty of free tools exist. This is table stakes, not innovation. | "No paywall, works on any phone browser." |

### After v1: AI features

The rule engine decides. AI only helps around it and never invents a skincare rule.

| # | Feature | Status |
|---|---|---|
| A1 | **Explain my routine**: an LLM rewords the engine's output in simple words | Build next |
| A2 | **Scan a label photo**: a vision model reads the ingredient list, my code matches the names, the user confirms | Build after A1 |
| A3 | **Ask SkinSync**: Q&A over the cited sources (RAG) | Later. Not being built now. |

### Later (not planned yet)

Cheaper product swaps, accounts with a database, skin-type and climate personalisation, barcode scan, user product submissions.

### Conflict rules table (v1 rule set)

Rules work on **ingredient families**, not single ingredients. Example: glycolic, lactic and mandelic acid all belong to the AHA family.

**Pair rules**

| ID | Family A | Family B | Type | Severity | What SkinSync does | Source |
|---|---|---|---|---|---|---|
| R1 | Retinoid | AHA (glycolic, lactic, mandelic) | Irritation | High | Different nights | [British Skin Foundation][bsf]; dermatologists advise acids on alternate nights to retinol ([Yahoo/Byrdie][yh]) |
| R2 | Retinoid | BHA (salicylic acid) | Irritation | Medium | Different nights if the BHA is leave-on. Allowed with a note if the BHA is a face wash. | Dermatologist advice: use acids as a cleanser or on alternate nights ([Yahoo/Byrdie][yh]) |
| R3 | Retinoid | Benzoyl peroxide | Deactivation + irritation | High | Benzoyl peroxide in AM, retinoid in PM | Lab study: benzoyl peroxide plus light destroyed over half of tretinoin in about 2 hours ([Martin et al. 1998, PubMed][martin]); AM/PM split from [British Skin Foundation][bsf] |
| R4 | Vitamin C (L-ascorbic acid) | Benzoyl peroxide | Deactivation | High | Different sessions (vitamin C in AM, benzoyl peroxide in PM) | [British Skin Foundation][bsf] |
| R5 | Vitamin C | Retinoid | Irritation | Medium | Vitamin C in AM, retinoid in PM | [British Skin Foundation][bsf] |
| R6 | Vitamin C | AHA | Irritation | Medium | Vitamin C in AM, AHA in PM | [British Skin Foundation][bsf] |
| R7 | Niacinamide | Vitamin C | **Myth, not a conflict** | Info | Allowed together. Shows a "common myth" note. | Cosmetic chemist review finds no loss of benefit or skin damage ([KindofStephen][kos]); [GoodRx][grx] |

**Timing rules (single family)**

| ID | Family | Rule | What SkinSync does | Source |
|---|---|---|---|---|
| T1 | Retinoid | Night only. Start on alternate nights. Needs sunscreen. | PM only. Beginner: at most 3 nights, never two running. Regular: up to nightly. | Start every other night and build up ([AAD][aad]); retinol is unstable in UV light ([dermatologist via AOL][aol]) |
| T2 | AHA (leave-on) | Raises sun sensitivity. Do not over-exfoliate. | PM only. Beginner 2 nights, regular 3, never two running. Warns if the shelf has no sunscreen. | FDA studies found AHAs increase UV sensitivity ([FDA][fda]); once or twice a week for dry or sensitive skin ([AAD news release][aadx]) |
| T3 | BHA (leave-on) | Do not over-exfoliate. | AM or PM. Beginner 2 days, regular 3, never two running. Face washes are not limited. | [AAD news release][aadx] |
| T4 | Vitamin C | Morning use is generally recommended. | AM only, can be daily. | [British Skin Foundation][bsf] |

Sunscreen is always placed in the AM as the last step. That is layering order in the code, not a rule in `rules.json`.

**Caveats you must know**

- **R3's study used tretinoin (a prescription retinoid), not retinol.** The same study found adapalene stayed stable. SkinSync applies R3 to retinol as a cautious default. Say this if asked.
- **The British Skin Foundation article was written by a pharmacist, not a dermatologist.** It is a reputable charity source but not a clinical trial.
- **Most rules are "irritation risk", not chemistry.** Skin tolerance varies. SkinSync is a planning aid, not medical advice. The UI needs a disclaimer.
- **The weekly limits for acids are my defaults.** The AAD says frequency depends on skin type and gives "once or twice a week" for dry or sensitive skin. Beginner = 2 follows that. Regular = 3 is my own middle setting, not a quoted number.
- **Vitamin C rules treat all forms alike.** The sources talk about "vitamin C". The catalogue's products use gentler derivatives (ethyl ascorbic acid, ascorbyl glucoside), so R4 to R6 are cautious for them.
- **Not yet sourced, so not in v1:** AHA + BHA used together, copper peptides + vitamin C. They go in only when a good source is found.

---

## Step 4: Comparison table

Legend: Yes = verified or claimed by the tool itself. No = verified no. ? = unverified.

| Feature | SkinSync v1 (planned) | INCIDecoder | SkinSort | CosDNA | Yuka | Skin Bliss | Skincare Routine (Mento) |
|---|---|---|---|---|---|---|---|
| Explains single ingredients | Basic (actives only) | Yes | Yes | Yes (scores) | Yes (risk) | Yes | ? |
| Flags conflicts between products | Yes | ? | Yes (claimed) | ? | No evidence | Yes | Yes |
| Shows the source for each conflict | Yes | n/a | ? | n/a | n/a | ? | ? |
| AM/PM routine | Yes | ? | Yes | ? | No evidence | Yes | Yes |
| Auto-schedules the week for you | Yes | ? | **No** | ? | No evidence | Partly (?) | Partly (orders steps; you pick days) |
| Beginner frequency limits for actives | Yes | ? | ? | ? | n/a | ? | ? |
| India-first catalogue with INR prices | Yes (30 products) | ? | Partial (user-submitted) | ? | **No** (not in India) | ? | No (DECIEM preloaded) |
| Catalogue size | Tiny | Large | Large | Large | About 2M cosmetics (third-party figure) | 100k+ | Small |
| Paste or scan any ingredient list | No (v2) | Yes | Yes | Yes | Barcode | Yes | No |
| Free | Yes | ? | Freemium | ? | Freemium | Freemium | Paid once |
| Login needed | No | No to browse | For routines | ? | ? | ? | ? |

**Where SkinSync loses:** catalogue size, ingredient depth, scanning, mobile app, personalisation. Do not hide this. The pitch is a narrow tool that does one job for one audience.

---

## Sources

**Competitors**

- [SkinSort: Routine Creator support doc][s1]
- [SkinSort: Routine Insights support doc][s2]
- [SkinSort vs SkinCarisma page][s3]
- [SkinSort on the App Store (prices)][s4]
- [SkinSort: user-submitted Indian products][s5]
- [SkinSort: example Indian-brand routine][s6]
- [INCIDecoder: About][i1] (the site redirected and would not load for me; details come from search snippets of this page)
- [CosDNA: rating scales][c1]
- [Yuka: app features][y1]
- [Yuka: country availability][y2]
- [Food Times: Yuka premium price][y3]
- [Skin Bliss on the App Store][b1]
- [Skincare Routine by Mento Apps on the App Store][m1]
- [SkinGuard on the App Store][g1]
- [SkinCare IQ][iq]
- [GlamGuider listing summary][gg]
- [SkinBB Label Looker press release][sb]
- [LoveSkin announcement][ls]
- [The Derma Co blog][dc]

**Conflict rules**

- [British Skin Foundation: which skincare you shouldn't mix][bsf]
- [Martin et al. 1998, Br J Dermatol: stability of tretinoin and adapalene with benzoyl peroxide][martin]
- [US FDA: Alpha Hydroxy Acids][fda]
- [American Academy of Dermatology: Retinoid or retinol?][aad]
- [KindofStephen (cosmetic chemist): niacinamide and vitamin C][kos]
- [GoodRx: can you mix niacinamide and vitamin C][grx]
- [Yahoo/Byrdie: AHAs/BHAs vs retinol, dermatologists explain][yh]
- [AOL: dermatologists on using retinol][aol]
- [AAD news release (via Newswise): Evaluate before you exfoliate][aadx]

[s1]: https://skinsort.com/support/the-routine-creator
[s2]: https://skinsort.com/support/skinsort-routine-insights
[s3]: https://www.skinsort.com/alternative/skincarisma
[s4]: https://apps.apple.com/app/id6478040418
[s5]: https://skinsort.com/users/preetidehingia/submitted-products
[s6]: https://skinsort.com/routine/h0tsl1g
[i1]: https://incidecoder.com/about
[c1]: https://www.cosdna.com/eng/help/ingredients_qna.php
[y1]: https://yuka.io/en/app
[y2]: https://help.yuka.io/l/en/article/v7vndx8ivc-availability-countries
[y3]: https://www.foodtimes.eu/?p=94430
[b1]: https://apps.apple.com/app/1385561364
[m1]: https://apps.apple.com/au/app/id1428570992
[g1]: https://apps.apple.com/app/id6758375131
[iq]: https://mira-krishnaiah.github.io/skincare-iq/frontend/
[gg]: https://mwm.ai/apps/glamguider-decode-beauty/6759090205
[sb]: https://cxotoday.com/press-release/skinbb-launches-indias-first-skincare-metaverse-merging-ai-technology-with-dermatological-expertise-for-consumer-empowerment/
[ls]: https://atavika.pages.dev/blog/introducing-loveskin
[dc]: https://thedermaco.com/blogs/skin-care/best-app-for-skin-care-products-in-india
[bsf]: https://www.britishskinfoundation.org.uk/which-pharmaceutical-skincare-you-shouldnt-mix-and-why
[martin]: https://pubmed.ncbi.nlm.nih.gov/9990414/
[fda]: https://www.fda.gov/cosmetics/cosmetic-ingredients/alpha-hydroxy-acids
[aad]: https://www.aad.org/public/everyday-care/skin-care-secrets/anti-aging/retinoid-retinol
[kos]: https://kindofstephen.com/can-you-use-niacinamide-and-vitamin-c-ascorbic/
[grx]: https://www.goodrx.com/health-topic/dermatology/can-you-mix-niacinamide-and-vitamin-c
[yh]: https://www.yahoo.com/lifestyle/ahas-bhas-vs-retinol-dermatologists-070400368.html
[aadx]: https://www.newswise.com/articles/evaluate-before-you-exfoliate
[aol]: https://www.aol.com/lifestyle/dermatologists-research-most-effective-skincare-175900992.html
