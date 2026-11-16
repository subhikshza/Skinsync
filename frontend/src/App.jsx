import { useEffect, useMemo, useState } from "react";
import { generateRoutine, getProducts, getRules } from "./api.js";

const TYPES = ["all", "cleanser", "toner", "serum", "moisturizer", "sunscreen"];
const SHELF_KEY = "skinsync.shelf";
const MAX_SHELF = 15;

// The shelf is kept in the browser so it survives a page refresh.
function loadShelf() {
  try {
    return JSON.parse(localStorage.getItem(SHELF_KEY)) || [];
  } catch {
    return [];
  }
}

export default function App() {
  const [products, setProducts] = useState([]);
  const [rules, setRules] = useState(null);
  const [shelf, setShelf] = useState(loadShelf);
  const [level, setLevel] = useState("beginner");
  const [routine, setRoutine] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([getProducts(), getRules()])
      .then(([p, r]) => {
        setProducts(p);
        setRules(r);
        // Drop saved ids that no longer exist in the catalogue.
        setShelf((s) => s.filter((id) => p.some((x) => x.id === id)));
      })
      .catch(() => setError("Could not reach the SkinSync server. Is the backend running?"));
  }, []);

  useEffect(() => {
    try {
      localStorage.setItem(SHELF_KEY, JSON.stringify(shelf));
    } catch {
      /* storage can be unavailable; the app still works */
    }
  }, [shelf]);

  function toggle(id) {
    setRoutine(null);
    setShelf((s) =>
      s.includes(id) ? s.filter((x) => x !== id) : s.length < MAX_SHELF ? [...s, id] : s
    );
  }

  async function build() {
    setLoading(true);
    setError("");
    try {
      setRoutine(await generateRoutine(shelf, level));
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <header>
        <h1>SkinSync</h1>
        <p>Pick the products you own. Get a week of morning and night routines with the clashing ones kept apart.</p>
      </header>

      {error && <p className="error" role="alert">{error}</p>}

      <ShelfPicker products={products} shelf={shelf} onToggle={toggle} />

      <section className="controls">
        <div className="level" role="group" aria-label="Experience level">
          <span>I am</span>
          {["beginner", "regular"].map((l) => (
            <button key={l} className={level === l ? "chip on" : "chip"}
              onClick={() => { setLevel(l); setRoutine(null); }}>
              {l === "beginner" ? "new to actives" : "used to actives"}
            </button>
          ))}
        </div>
        <button className="primary" disabled={!shelf.length || loading} onClick={build}>
          {loading ? "Building…" : `Build my week (${shelf.length} product${shelf.length === 1 ? "" : "s"})`}
        </button>
      </section>

      {routine && (
        <>
          <Warnings items={routine.warnings} />
          <WeekGrid days={routine.days} />
          <Plan plan={routine.plan} />
          <Conflicts conflicts={routine.conflicts} />
        </>
      )}

      {rules && <RulesPanel rules={rules} />}

      <footer>
        SkinSync is a planning aid based on general published guidance. It is not medical advice.
        Skin differs from person to person, so patch test new products and see a dermatologist for skin conditions.
      </footer>
    </div>
  );
}

function ShelfPicker({ products, shelf, onToggle }) {
  const [query, setQuery] = useState("");
  const [type, setType] = useState("all");

  const visible = useMemo(
    () =>
      products.filter(
        (p) =>
          (type === "all" || p.type === type) &&
          `${p.brand} ${p.name}`.toLowerCase().includes(query.toLowerCase())
      ),
    [products, query, type]
  );

  return (
    <section>
      <h2>1. Your shelf</h2>
      <div className="filters">
        <input type="search" placeholder="Search brand or product" value={query}
          onChange={(e) => setQuery(e.target.value)} aria-label="Search products" />
        {TYPES.map((t) => (
          <button key={t} className={type === t ? "chip on" : "chip"} onClick={() => setType(t)}>
            {t}
          </button>
        ))}
      </div>
      <div className="grid">
        {visible.map((p) => {
          const picked = shelf.includes(p.id);
          return (
            <button key={p.id} className={picked ? "card picked" : "card"}
              aria-pressed={picked} onClick={() => onToggle(p.id)}>
              <span className="brand">{p.brand}</span>
              <span className="name">{p.name}</span>
              <span className="meta">{p.type} · ₹{p.price_inr}</span>
              {p.actives.length > 0 && (
                <span className="actives">{p.actives.map((a) => a.replaceAll("-", " ")).join(", ")}</span>
              )}
            </button>
          );
        })}
        {!visible.length && <p className="muted">No products match.</p>}
      </div>
    </section>
  );
}

function Warnings({ items }) {
  if (!items.length) return null;
  return (
    <section className="warnings" role="status">
      {items.map((w) => <p key={w}>⚠ {w}</p>)}
    </section>
  );
}

function WeekGrid({ days }) {
  return (
    <section>
      <h2>2. Your week</h2>
      <div className="week">
        {days.map((d) => (
          <div key={d.day} className="day">
            <h3>{d.day}</h3>
            <Slot title="AM" steps={d.am} />
            <Slot title="PM" steps={d.pm} />
          </div>
        ))}
      </div>
    </section>
  );
}

function Slot({ title, steps }) {
  return (
    <div className={`slot ${title.toLowerCase()}`}>
      <h4>{title}</h4>
      {steps.length ? (
        <ol>
          {steps.map((s) => (
            <li key={s.product_id} className={`step ${s.type}`}>
              <span className="brand">{s.brand}</span> {s.name}
            </li>
          ))}
        </ol>
      ) : (
        <p className="muted">Nothing</p>
      )}
    </div>
  );
}

function Plan({ plan }) {
  return (
    <section>
      <h2>3. Why each product is where it is</h2>
      <table>
        <thead>
          <tr><th>Product</th><th>When</th><th>Why</th></tr>
        </thead>
        <tbody>
          {plan.map((p) => (
            <tr key={p.product_id}>
              <td>{p.name}</td>
              <td>{p.slots.join(" + ") || "Not used"}{p.days.length === 7 ? ", daily" : p.days.length ? `, ${p.days.join(" ")}` : ""}</td>
              <td>{p.reasons.join(". ")}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}

function Conflicts({ conflicts }) {
  return (
    <section>
      <h2>4. Conflicts found ({conflicts.length})</h2>
      {!conflicts.length && <p className="muted">None. These products can be used together.</p>}
      {conflicts.map((c) => (
        <article key={c.rule_id + c.product_a + c.product_b} className={`conflict ${c.severity}`}>
          <h3>
            <span className="badge">{c.type === "myth" ? "myth" : c.severity}</span>
            {c.product_a_name} + {c.product_b_name}
          </h3>
          <p>{c.explanation}</p>
          {c.resolved_how && <p><strong>What SkinSync did:</strong> {c.resolved_how}</p>}
          <p className="source">
            Rule {c.rule_id} · Source:{" "}
            <a href={c.source_url} target="_blank" rel="noreferrer">{c.source_title}</a>
          </p>
        </article>
      ))}
    </section>
  );
}

function RulesPanel({ rules }) {
  return (
    <details className="rules">
      <summary>How SkinSync decides (all {rules.conflicts.length + rules.timing.length} rules and their sources)</summary>
      <table>
        <thead>
          <tr><th>Rule</th><th>Applies to</th><th>What it says</th><th>Source</th></tr>
        </thead>
        <tbody>
          {rules.conflicts.map((r) => (
            <tr key={r.id}>
              <td>{r.id}</td>
              <td>{r.family_a.replace("_", " ")} + {r.family_b.replace("_", " ")}</td>
              <td>{r.explanation}</td>
              <td><a href={r.source_url} target="_blank" rel="noreferrer">{r.source_title}</a></td>
            </tr>
          ))}
          {rules.timing.map((r) => (
            <tr key={r.id}>
              <td>{r.id}</td>
              <td>{r.family.replace("_", " ")}</td>
              <td>{r.explanation}</td>
              <td><a href={r.source_url} target="_blank" rel="noreferrer">{r.source_title}</a></td>
            </tr>
          ))}
        </tbody>
      </table>
    </details>
  );
}
