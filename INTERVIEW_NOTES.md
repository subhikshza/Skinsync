# SkinSync — Interview Notes

_Living document. Updated at every stage. Last update: 16 Nov 2026, Phase 2 step 1: v1 is built (backend, frontend, 30 products). AI features are not built yet._

Related docs: `docs/PHASE1_RESEARCH.md` (competitors, rules, sources) and `docs/ARCHITECTURE.md` (design, diagrams).

---

## 1. 30-second pitch

> "SkinSync is a web app for Indian students who are new to skincare actives. You pick the products you already own, and it tells you which ones clash and builds a 7-day morning and night routine that keeps the clashing ones apart. Every rule it uses links to a dermatology or cosmetic-chemistry source. Tools like SkinSort make you plan the week by hand and are not built around products sold in India. I built it with React and FastAPI, with a rule engine I can explain line by line."

**The problem statement in 2 lines (learn this one):**

> Indian students who are new to skincare actives buy several products and do not know which ones clash or how to space them across the week.
> Other tools explain ingredients or flag a clash; SkinSync builds the whole AM/PM week for you from products sold in India, and shows the source behind every rule.

The three differences packed into line 2: it **plans** (not only warns), it is built for the **Indian shelf**, and its rules are **sourced**.

**Longer version (for the README):**

> Indian college students and first-time skincare users are buying active-ingredient products (retinol, salicylic acid, vitamin C, niacinamide) from affordable brands like Minimalist and Deconstruct, mostly on advice from Instagram and friends. They do not know which actives can share a routine, so they either layer everything every night and irritate their skin, or avoid useful products because of myths. Existing tools mostly explain one product at a time, or flag a clash and leave the user to work out the weekly schedule; the ones that go further are subscription apps not built around the Indian market. SkinSync takes the products a user already owns and returns a conflict-free AM/PM plan for the whole week, with every rule linked to its source.

---

## 2. How it works (big picture)

1. The user opens the site. The app loads the product catalogue from the server.
2. The user ticks the products they own (their "shelf") and picks beginner or regular.
3. The app sends the product ids to the server.
4. The server looks up each product's active ingredients and maps them to families (for example, glycolic acid belongs to the AHA family).
5. The conflict engine checks every pair of products against the rules table.
6. The scheduler puts each product in AM or PM, splits clashing night products onto different nights, and limits how often strong actives appear.
7. The server sends back a 7-day plan, the list of conflicts, and any warnings.
8. The app shows a week grid and a card for each conflict with its reason and source link.

```
User -> React app -> FastAPI -> conflict engine -> scheduler -> 7-day plan -> React app
                                    |                 |
                              ingredients.json    rules.json (with sources)
```

---

## 3. Differentiators (and the honest version)

**Important:** conflict checkers and routine builders already exist (Skin Bliss, Mento's Skincare Routine app, SkinGuard, a student project called SkinCare IQ). Never say "nothing like this exists". Say "better for X".

| # | What | Honest status | Say it like this |
|---|---|---|---|
| D1 | Auto-built weekly schedule | SkinSort's routine creator is manual; its docs list auto-generation as a future idea. Some smaller apps do parts of this. | "Most tools give a warning. Mine gives the plan." |
| D2 | Every rule has a source and a reason type | One student project also claims cited rules. I did not find it in mainstream apps. | "You can click any warning and see where it came from." |
| D3 | India-first catalogue, rupee prices | v1 has about 30 products. Small. | "It starts from what an Indian student actually has on the shelf." |
| D4 | Beginner frequency limits | Standard dermatology advice, built into the scheduler. | "A beginner gets retinol on alternate nights, not every night." |
| D5 | Free, no login | Common. Not an innovation. | Only mention if asked about cost. |

**v2 ideas (not built):** the three AI features in section 4, cheaper product swaps, accounts with a database, skin-type and climate personalisation.

---

## 4. AI features (planned, after v1)

**The one idea behind all three:** the rule engine decides, the AI only helps around it. The AI never invents a skincare rule. That is the line to hold in an interview.

| # | Feature | What it does | Difficulty | Build order |
|---|---|---|---|---|
| A1 | **Explain my routine** | Turns the engine's output (conflicts, schedule, rule text) into a short friendly explanation: "Why is retinol only on Mon, Wed, Fri?" | **Easy.** About 2 to 3 hours. One new endpoint and one prompt. | **First, right after v1** |
| A2 | **Scan a label photo** | User uploads a photo of the ingredient list. A vision model reads the text. My code matches the names to `ingredients.json`. User confirms before it joins the shelf. | **Medium to hard.** About 6 to 10 hours. Needs a bigger ingredient list with aliases, fuzzy matching, and a confirm screen. | Second |
| A3 | **Ask SkinSync (Q&A with citations)** | A chat box that answers skincare questions only from my cited sources, with links. This is RAG. | **Hard.** About 10 to 15 hours. Chunking, embeddings, a vector store, and testing answer quality. | **Later. Not being built now.** |

### A1. Explain my routine (recommended first)

- **How it works:** the server runs the engine as usual, then sends the result as JSON to an LLM with the instruction "explain this in simple words, use only the facts given". If the LLM call fails, the app shows the plain rule text instead.
- **Why first:** it sits directly on top of what v1 already produces, it is the cheapest to build, and the risk of made-up advice is low because the model only rewords facts I give it.
- **Honest weakness:** on its own this is a thin layer over an LLM, and an interviewer may say so. The defence is the design around it: grounding, a fallback, and a small test set (for example 10 shelves, checking the explanation never names an ingredient that was not in the input).
- **Do not call this RAG.** Nothing is retrieved from a document store. The correct term is grounded generation, or structured-context prompting.
- **Say it like this:** "The rule engine makes every decision. The LLM only rewrites the engine's output in plain language, using facts I pass in. If the model is down, the user still gets the rule text. I check it with a small test set so it cannot add ingredients or rules."

### A2. Scan a label photo

- **How it works:** photo, then a vision-capable LLM (or OCR) extracts the ingredient text, then my own code cleans the names and matches them against known ingredients and aliases, then the user confirms the detected actives.
- **Why it matters:** it fixes v1's biggest weakness. Any product works, not only the 30 in my catalogue.
- **Honest status:** not new. INCIDecoder says it can analyse an ingredient list from a photo, and SkinSort has a scanner. For SkinSync it is catching up, not standing out.
- **Hard parts:** blurry photos, labels that list only "key ingredients", spelling variants, and a wrong match silently producing a wrong routine. That is why the confirm step exists.
- **Say it like this:** "The model only reads text off the photo. Matching is my own deterministic code, and the user confirms before anything reaches the engine, so one misread cannot change the advice silently."

### A3. Ask SkinSync (RAG) — later, not being built now

- **How it works:** split my source notes into chunks, turn them into embeddings, store them in a vector database, fetch the closest chunks for a question, and have the LLM answer only from those chunks with links.
- **Why last:** most work, and the highest risk, because open questions drift into medical advice. It needs refusals for anything outside the sources.
- **Overlap warning:** CampusGPT is already a document Q&A idea. If that gets built, RAG is better shown there, and SkinSync does not need it.
- **Say it like this:** "It is retrieval-augmented generation. I fetch the relevant passages from my own cited sources first and the model answers only from those, with citations, and refuses when the sources do not cover the question."

**Not decided yet:** which LLM provider. Pick at build time and check the free tier then. Keep the API key on the server, never in the React app.

---

## 5. Decision log

### D-01: Scope v1 to "shelf in, weekly plan out"
- **Chose:** Curated catalogue, conflict check, weekly schedule. Nothing else.
- **Alternatives:** Ingredient-list scanner, AI chatbot, product recommendations.
- **Why:** About 14 hours of build time. The rule engine and scheduler are the part I can defend in depth.
- **Trade-off:** Users can only pick products that are in my catalogue.
- **Say it like this:** "I cut it to the one job existing tools make you do by hand, and listed everything else as v2."

### D-02: Rule-based engine, not AI, for conflicts
- **Chose:** A fixed rules table with sources.
- **Alternatives:** Ask an LLM "do these clash?"; train a model.
- **Why:** Skincare advice must be the same every time and traceable to a source. An LLM can make things up. There is also no dataset to train on.
- **Trade-off:** It only knows the rules I entered. New ingredients need manual work.
- **Say it like this:** "For safety advice I wanted answers I can trace. AI comes in v2 to explain the rules, not to invent them."

### D-03: Rules on ingredient families, not single ingredients
- **Chose:** Group ingredients into families (retinoid, AHA, BHA, vitamin C, benzoyl peroxide, niacinamide).
- **Alternatives:** One rule per ingredient pair.
- **Why:** Seven rules cover dozens of ingredients. Adding lactic acid means adding it to the AHA family, with no new rule.
- **Trade-off:** Loses detail. Mandelic acid is gentler than glycolic, but both count as AHA.
- **Say it like this:** "Families keep the rule table small and easy to check against sources."

### D-04: Rules stored as data (JSON), not written in code
- **Chose:** `rules.json` with a source URL on every rule.
- **Alternatives:** if/else statements in Python.
- **Why:** A rule can be added or fixed without touching the logic. The same file feeds a "how it decides" page.
- **Trade-off:** Needs validation so a typo in the file does not break things. Pydantic does that at startup.
- **Say it like this:** "The engine is generic. The knowledge lives in a data file anyone can review."

### D-05: Niacinamide + vitamin C is marked as a myth, not a conflict
- **Chose:** Allow them together and show a "common myth" note.
- **Alternatives:** Flag it like some apps do.
- **Why:** Cosmetic chemists who reviewed the evidence found no loss of benefit and no skin damage. Flagging it would spread the myth.
- **Trade-off:** Some users expect a warning and may doubt the tool. The note with a source handles that.
- **Say it like this:** "I only added rules I could source. This one I could source as false."
- **Source:** KindofStephen (cosmetic chemist) and GoodRx, linked in `PHASE1_RESEARCH.md`.

### D-06: React + Vite for the frontend
- **Chose:** React with Vite.
- **Alternatives:** Next.js, plain HTML and JavaScript.
- **Why:** I know React. Vite needs no setup. The app has three screens and needs no server rendering or SEO.
- **Trade-off:** No server-side rendering.
- **Say it like this:** "It is a small interactive tool, so a plain React single-page app was enough."

### D-07: FastAPI for the backend
- **Chose:** FastAPI.
- **Alternatives:** Flask, Express, or no backend at all (all logic in the browser).
- **Why:** Pydantic validates requests and my data files. Free interactive API docs. Python makes the engine easy to test, and v2's AI features need a server to hold API keys.
- **Trade-off:** One more thing to deploy. For v1 alone, doing it all in the browser would have worked.
- **Say it like this:** "FastAPI gave me validation and docs for free, and it sets up the AI work in v2. I know v1 could have run fully in the browser."

### D-08: JSON files instead of a database
- **Chose:** Three JSON files loaded into memory when the server starts.
- **Alternatives:** SQLite, PostgreSQL, MongoDB.
- **Why:** The data is small, read-only and hand-written. Git shows who changed which rule and why.
- **Trade-off:** No user accounts or saved routines on the server. Does not scale to thousands of products or user edits.
- **Say it like this:** "There was nothing to write, so a database would have been setup with no benefit. When accounts arrive I would move to Postgres."

### D-09: User's shelf saved in the browser (localStorage)
- **Chose:** localStorage.
- **Alternatives:** Accounts and a database.
- **Why:** Keeps the shelf between visits without building login.
- **Trade-off:** Clearing the browser or switching device loses it.
- **Say it like this:** "No login means no personal data on my server, and less to build."

### D-10: Scheduling as a conflict graph with a greedy day-by-day pass
- **Chose:** Work out which pairs of actives must not share a day, then fill Monday to Sunday one day at a time. Each day, take the actives in turn (fewest days so far goes first) and skip any that hit its weekly limit, was used yesterday, or clashes with one already placed that day.
- **Alternatives:** Try every possible week (brute force); a constraint solver library such as OR-Tools; grouping actives into "night groups" first (my Phase 1 design).
- **Why:** A shelf has about five actives. Greedy is about 15 lines, runs instantly, and I can trace it by hand. Day-by-day also handles clashes across AM and PM, which night groups did not.
- **Trade-off:** Greedy does not promise the best possible week. At this size every case I tested came out sensible.
- **Say it like this:** "It is a small constraint problem on a conflict graph, related to graph colouring, which is NP-hard in general. With five nodes I chose a greedy pass I can explain over a solver I cannot."

### D-11: Wash-off products are treated as lower risk
- **Chose:** A salicylic acid face wash with a retinol serum gives an info note, not a hard split.
- **Alternatives:** Treat every product the same.
- **Why:** Dermatologists suggest using acids as a cleanser or on alternate nights when on retinol. A cleanser is on the skin for under a minute.
- **Trade-off:** Very sensitive skin may still react.
- **Say it like this:** "The rule looks at how the product is used, not only what is in it."

### D-12: Stateless API
- **Chose:** The server remembers nothing between requests.
- **Alternatives:** Sessions.
- **Why:** Every request carries the product ids it needs. Simple to test and deploy.
- **Trade-off:** The client resends the shelf every time. It is a few ids, so no cost.
- **Say it like this:** "Same input always gives the same output, which made testing simple."

### D-13: Claim "sold in India", not "Indian brands only"
- **Chose:** Catalogue = products available in India with rupee prices, plus a `brand_origin` field.
- **Alternatives:** Only Indian-founded brands.
- **Why:** My own seed data includes Simple, Garnier, Tonymoly and The Ordinary. Real Indian shelves are mixed.
- **Trade-off:** "Indian brands" was a punchier line.
- **Say it like this:** "It is built around what is on shelves in India, whoever makes it."

### D-14: First AI feature is "Explain my routine", not label scanning or RAG
- **Chose:** A1, an LLM that rewords the engine's output.
- **Alternatives:** A2 label photo scan; A3 RAG question answering.
- **Why:** Smallest build on top of v1, lowest risk of made-up advice, and it shows the pattern I want to defend: fixed logic decides, AI explains.
- **Trade-off:** Least impressive of the three by itself. A2 is the one that makes the product more useful, so it comes second.
- **Say it like this:** "I added AI where a mistake is cheap, explaining, before adding it where a mistake changes the advice, reading labels."

### D-15: Split products into "actives" and "basics"
- **Chose:** An active is a leave-on product with a strong family (retinoid, AHA, BHA, vitamin C, benzoyl peroxide). Everything else, including every cleanser, is a basic that goes on daily.
- **Alternatives:** Schedule every product with the same logic.
- **Why:** Only a few products need careful placing. Treating the rest as daily keeps the scheduler short.
- **Trade-off:** A niacinamide serum is "basic", so it shows up morning and night every day. Fine for niacinamide, but it is a simplification.
- **Say it like this:** "I only run the hard logic on the products that need it."

### D-16: A face wash that truly clashes is moved, not ignored
- **Chose:** A benzoyl peroxide face wash with a retinol serum: the wash is kept to the morning. If it clashes in both morning and night, it is left out with a warning.
- **Alternatives:** Treat all face washes as harmless; or schedule them like serums.
- **Why:** The benzoyl peroxide rule is about deactivation, and the sourced advice is "benzoyl peroxide in the morning, retinoid at night". Only the salicylic acid rule has a source for relaxing face washes.
- **Trade-off:** Leaving a product out is cautious and may annoy a user.
- **Say it like this:** "I relaxed a rule for face washes only where a source said so."

### D-17: Two levels, beginner and regular
- **Chose:** One toggle that changes weekly limits (beginner retinol: 3 nights, never two running; regular: up to nightly).
- **Alternatives:** Full skin-type quiz; no levels at all.
- **Why:** Dermatology advice for retinoids is "start slow and build up". One toggle captures that without building a profile system.
- **Trade-off:** Beginner 2 and regular 3 for acids are my defaults. The AAD only says frequency depends on skin type.
- **Say it like this:** "The limits live in the rules file, so changing them is a data edit, not a code change."

### D-18: Catalogue records headline actives and MRP, each with a source link
- **Chose:** For each product: the actives the brand names, the MRP on the source page on 16 Nov 2026, and the page URL.
- **Alternatives:** Full ingredient lists; live prices from an API.
- **Why:** Headline actives are what the rules need, and they can be checked quickly. Checking found a mistake in my seed data: the Deconstruct gel sunscreen has no niacinamide on the brand page.
- **Trade-off:** Minor ingredients are missed, and prices go stale.
- **Say it like this:** "Every product row links to where I got it, the same standard as the rules."

**Shortcut to own up to:** the catalogue is typed in by hand from product pages. That will not scale. Good answer: "v1 proves the engine. Catalogue growth is a v2 problem, through pasted ingredient lists or user submissions."

---

## 6. Each part explained

| Part | File | What it does | Connects to |
|---|---|---|---|
| Catalogue | `data/products.json` | 30 products: name, brand, type, MRP, actives, source link | Served to the shelf picker |
| Ingredients | `data/ingredients.json` | Maps each active to a family | Read by the engine |
| Rules | `data/rules.json` | 7 conflict rules, 4 timing rules, each with a source | Read by engine and scheduler |
| Models | `backend/app/models.py` | Pydantic shapes for data files, requests and responses | Used everywhere |
| Engine | `backend/app/engine.py` | `Catalog` loads and checks the data. `detect_conflicts` checks every pair of products. | Called by scheduler and API |
| Scheduler | `backend/app/scheduler.py` | `build_week` builds the 7-day plan | Called by the API |
| API | `backend/app/main.py` | 7 routes. Validates input, calls the engine, returns JSON | Talks to the React app |
| Tests | `backend/tests/test_engine.py` | 18 pytest tests | Run with `pytest` in `backend/` |
| Frontend | `frontend/src/App.jsx`, `api.js` | Shelf picker, week grid, reasons table, conflict cards, rules panel | Calls the API, saves shelf in localStorage |

**How to run it**

```
# terminal 1
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload        # http://localhost:8000/docs

# terminal 2
cd frontend
npm install
npm run dev                          # http://localhost:5173
```

---

## 7. Key code to know

### 7.1 Finding conflicts (`engine.py`)

```python
for p1, p2 in combinations(products, 2):          # every pair, once
    for f1 in catalog.families_of(p1):            # e.g. {"retinoid"}
        for f2 in catalog.families_of(p2):        # e.g. {"aha"}
            # frozenset means the order of the two families does not matter
            rule = catalog.rule_by_pair.get(frozenset((f1, f2)))
            if rule is None:
                continue                          # no rule, no conflict
            # a face wash is on the skin briefly, so some rules are relaxed
            wash_off = rule.skip_if_wash_off and "cleanser" in (p1.type, p2.type)
            found.append(Conflict(..., severity="info" if wash_off else rule.severity))
```

### 7.2 Which pairs must not share a day (`scheduler.py`)

```python
for c in real:                                    # conflicts that need action
    a, b = c.product_a, c.product_b
    # same slot = they would touch; "separate_days" = keep apart even across AM/PM
    if slot[a] == slot[b] or c.resolution == "separate_days":
        blocked[a].add(b)                         # a line in the conflict graph
        blocked[b].add(a)
    else:
        c.resolved_how = "Used in different routines ..."   # AM vs PM is enough
```

### 7.3 Placing actives day by day (`scheduler.py`) — the heart of the project

```python
for d in range(7):                                # Monday to Sunday
    today = []
    # fewest days so far goes first, so clashing actives take turns
    for p in sorted(actives, key=lambda p: (len(on[p.id]), priority(p), p.id)):
        if len(on[p.id]) >= cap[p.id]:
            continue                              # weekly limit reached
        if no_consec[p.id] and (d - 1 in on[p.id] or (d == 6 and 0 in on[p.id])):
            continue                              # used yesterday (Sun also checks Mon)
        if blocked[p.id] & set(today):
            continue                              # clashes with one already placed today
        today.append(p.id)
        on[p.id].append(d)
```

### 7.4 Loading data safely (`engine.py`)

```python
self.products = {p["id"]: Product(**p) for p in load("products.json")}   # Pydantic checks each row
for p in self.products.values():
    for a in p.actives:
        if a not in self.ingredients:             # a typo in the data file
            raise ValueError(f"{p.id}: unknown ingredient '{a}'")       # server refuses to start
```

---

## 8. Terms to know

| Term | One-line meaning |
|---|---|
| Active | An ingredient that changes the skin, like retinol. Not a filler. |
| INCI | The standard naming system for cosmetic ingredients on labels. |
| Retinoid | Vitamin A family (retinol, tretinoin, adapalene). Speeds up skin renewal. |
| AHA | Alpha hydroxy acid (glycolic, lactic). Exfoliates the skin surface. |
| BHA | Beta hydroxy acid (salicylic acid). Exfoliates inside pores. |
| Benzoyl peroxide | Acne treatment that kills bacteria by oxidising. |
| Niacinamide | Vitamin B3. Gentle, mixes with most things. |
| Ingredient family | My grouping of similar actives so one rule covers all of them. |
| Rule engine | Code that applies a table of if-this-then-that rules to data. |
| Graph colouring | Giving labels to connected items so no two connected items share a label. |
| Greedy algorithm | Makes the best choice at each step without looking back. |
| NP-hard | A class of problems with no known fast exact method for large inputs. |
| Pydantic | Python library that checks data has the right shape and types. |
| Stateless | The server keeps no memory of earlier requests. |
| localStorage | Small key-value storage inside the user's browser. |
| Pure function | Same input always gives the same output, and it changes nothing else. |
| RAG | Retrieval-augmented generation: fetch relevant passages first, then have the LLM answer from them. (A3) |
| Grounded generation | The LLM is given the facts and told to use only those. (A1) |
| Hallucination | An LLM stating something false with confidence. |
| Embedding | A list of numbers that represents the meaning of a piece of text, used to find similar text. |
| Fuzzy matching | Matching text that is close but not identical, such as spelling variants. |
| Human in the loop | A person confirms the AI's output before it is used. |

---

## 9. Limitations and next steps

- **Small catalogue.** 30 products. If a product is missing, the tool cannot help. (A2 is meant to fix this.)
- **Only headline actives.** It does not read the full ingredient list.
- **No concentrations.** 0.3% retinol and 1% retinol are treated the same.
- **Vitamin C forms are treated alike.** The catalogue's products use gentler derivatives, so the vitamin C rules are cautious for them.
- **Rules are general advice.** Most are "irritation risk" and skin differs between people. Not medical advice.
- **One rule is extrapolated.** The benzoyl peroxide study used tretinoin, not retinol. Adapalene was stable in the same study.
- **Acid limits are my defaults.** Beginner 2 follows AAD wording for sensitive skin. Regular 3 is my own setting.
- **Two rules left out** because I could not source them well: AHA + BHA together, copper peptides + vitamin C.
- **Greedy scheduler.** Not guaranteed to find the best week. Fixed Monday start.
- **Not deployed.** Runs locally. No frontend tests.
- **Prices go stale.** MRPs were read on 16 Nov 2026.
- **Competitor claims are from public pages.** I did not use every app. Anything marked "unverified" in the research doc stays unverified.
- **Next:** AI features A1 then A2 (section 4). Later: A3, deployment, accounts with Postgres, product swaps.

---

## 10. Likely interview questions

**1. What problem does SkinSync solve?**
Beginners in India buy several active products and do not know which can be used together. SkinSync finds the clashes and builds a weekly morning and night plan that avoids them.

**2. SkinSort and Skin Bliss already exist. Why build this?**
They do exist, and some check conflicts. SkinSort makes you schedule the week by hand, the deeper features are paid, and none is built around products sold in India. Mine auto-builds the week, shows a source for every rule, and starts from an Indian shelf. It is a narrower tool, not a bigger one.

**3. Where do your conflict rules come from? How do I know they are right?**
Every rule has a source: the British Skin Foundation, the American Academy of Dermatology, the US FDA, a 1998 British Journal of Dermatology study, and a cosmetic chemist's review. I left out rules I could not source. The app links each warning to its source.

**4. Why not use an LLM to detect conflicts?**
It can give different answers each time and can make things up, which is risky for skin advice. A rules table is predictable and testable. I plan to use an LLM in v2 only to explain the rules in plain language, grounded in the same sources.

**5. How does the scheduling algorithm work?**
Basics go on every day. Each active gets AM or PM from timing rules, for example retinol at night. Then I work out which pairs must not share a day, and fill the week one day at a time: each day I take the actives in turn and skip any that hit its weekly limit, was used the day before, or clashes with one already placed that day. A beginner ends up with retinol Mon, Wed, Fri and an AHA on Tue, Thu.

**6. Why JSON files and not a database?**
The data is small, read-only and written by hand. There is nothing to write back. JSON in git also gives me a history of every rule change. I would add Postgres when user accounts and saved routines come in.

**7. Why FastAPI over Flask, or over no backend?**
FastAPI validates data with Pydantic and generates API docs. Versus no backend: v1 could run in the browser, but the engine is easier to test in Python and v2's AI features need a server for API keys.

**8. What happens with 100,000 products or many users?**
Conflict checking only looks at the user's shelf, about ten products, so that part does not slow down. The catalogue would move to a database with search and paging. The server is stateless, so more copies can run behind a load balancer.

**9. What was the hardest part?**
Two things. First, being honest about what was new: research showed several conflict checkers exist, so I had to find the narrower gap. Second, the edge cases in scheduling. For example a benzoyl peroxide face wash clashes with vitamin C in the morning and retinol at night, so there is nowhere to put it. My first version said "use it in the morning" and also left it out. A test caught that, and now it is left out with a clear warning.

**10. How did you test it?**
18 pytest tests on the pure functions and the API. For example: retinol and glycolic acid never land on the same night; retinol is never in the morning; a beginner never gets retinol two nights running, including Sunday into Monday; niacinamide plus vitamin C is only a myth note; the same input always gives the same output. I also clicked through the built app in a headless browser.

**11. What are its limitations?**
Small catalogue, only main actives, no concentrations, general rules rather than personal advice. It is a planning aid, not a dermatologist.

**12. What would you add next?**
First an LLM that explains the routine in plain words, using only the engine's output. Then label photo scanning so any product works, with a confirm step.

**13. Where is the AI in this project? Why is the core not AI?**
v1 has none, on purpose. Skin advice has to be repeatable and traceable, so rules decide. AI comes in around the engine: explaining the result, and reading labels. It never creates a rule.

**14. How do you stop the LLM from making things up?**
It only gets the engine's output and is told to use nothing else. I test it on a fixed set of shelves to check it adds no new ingredient or rule, and if the call fails the app falls back to the plain rule text.

---

## 11. Explain-it-back checklist

Tick these off when you can explain each one without notes. Start with the 2-line problem statement.

- [ ] The problem and who it is for, in three sentences
- [ ] Two competitors, what each does, and the gap SkinSync fills (without overclaiming)
- [ ] Why rules are data with sources, and why not an LLM
- [ ] The three AI features, why A1 goes first, and why A1 is not RAG
- [ ] The scheduler: AM/PM slots, blocked pairs, weekly limits, the day-by-day loop (snippet 7.3)
- [ ] Why JSON files now and what would make you switch to a database

---

## Changelog

- **16 Nov 2026, Phase 1:** Created. Problem statement, differentiators, decisions D-01 to D-13, 12 questions. No code yet.
- **16 Nov 2026, before Phase 2:** Added the 2-line problem statement, section 4 (three AI features, A1 recommended first), decision D-14, questions 13 and 14, six glossary terms. Sections after 4 renumbered.
- **16 Nov 2026, Phase 2 step 1:** v1 built. 30 products with source links, backend (engine, scheduler, 7 routes, 18 tests), React frontend. D-10 rewritten (day-by-day greedy), D-15 to D-18 added, sections 6 and 7 filled with real files and code, A3 marked as later.
