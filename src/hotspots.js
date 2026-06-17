
/*
B3 hotspot ranking layer.

This file is independent from app.js on purpose.
It reads public/data/country_hotspots.csv and renders a compact ranking layer.
*/

(function () {
  const HOTSPOT_DATA_URL = "public/data/country_hotspots.csv";

  function parseCSV(text) {
    const rows = [];
    const lines = text.replace(/^\uFEFF/, "").split(/\r?\n/).filter(line => line.trim() !== "");
    if (!lines.length) return rows;

    const delimiter = lines[0].includes(";") && !lines[0].includes(",") ? ";" : ",";
    const header = splitLine(lines[0], delimiter).map(h => h.trim());

    for (let i = 1; i < lines.length; i++) {
      const values = splitLine(lines[i], delimiter);
      const row = {};
      header.forEach((h, idx) => row[h] = (values[idx] || "").trim());
      rows.push(row);
    }
    return rows;
  }

  function splitLine(line, delimiter) {
    const out = [];
    let cur = "";
    let inQuotes = false;

    for (let i = 0; i < line.length; i++) {
      const ch = line[i];

      if (ch === '"') {
        if (inQuotes && line[i + 1] === '"') {
          cur += '"';
          i++;
        } else {
          inQuotes = !inQuotes;
        }
      } else if (ch === delimiter && !inQuotes) {
        out.push(cur);
        cur = "";
      } else {
        cur += ch;
      }
    }
    out.push(cur);
    return out;
  }

  function num(value) {
    if (value === undefined || value === null || value === "") return null;
    const n = Number(String(value).replace(",", "."));
    return Number.isFinite(n) ? n : null;
  }

  function fmtKt(value) {
    const n = num(value);
    if (n === null) return "no data";
    if (n >= 1000) return `${(n / 1000).toFixed(1)} Mt CO₂e`;
    return `${Math.round(n)} kt CO₂e`;
  }

  function fmtHa(value) {
    const n = num(value);
    if (n === null) return "no data";
    if (n >= 1000000) return `${(n / 1000000).toFixed(1)} Mha`;
    if (n >= 1000) return `${Math.round(n / 1000)} kha`;
    return `${Math.round(n)} ha`;
  }

  function fmtDensity(value) {
    const n = num(value);
    if (n === null) return "no data";
    return `${n.toFixed(1)} t CO₂e/ha`;
  }

  function completeRows(rows) {
    return rows.filter(r => num(r.emissions_total_kt_co2e) !== null);
  }

  function topBy(rows, field, n = 10) {
    return [...rows]
      .filter(r => num(r[field]) !== null)
      .sort((a, b) => num(b[field]) - num(a[field]))
      .slice(0, n);
  }

  function barWidth(value, max) {
    const n = num(value);
    if (n === null || !max) return 0;
    return Math.max(2, Math.min(100, (n / max) * 100));
  }

  function renderRanking(container, rows, field, label, formatter) {
    const top = topBy(rows, field, 10);
    const max = top.length ? num(top[0][field]) : 0;

    container.innerHTML = top.map((r, idx) => `
      <article class="hotspot-row">
        <div class="hotspot-rank">${idx + 1}</div>
        <div class="hotspot-main">
          <div class="hotspot-row-head">
            <strong>${r.country}</strong>
            <span>${formatter(r[field])}</span>
          </div>
          <div class="hotspot-bar-wrap" aria-label="${label}">
            <div class="hotspot-bar" style="width:${barWidth(r[field], max)}%"></div>
          </div>
          <p>
            Area: ${fmtHa(r.drained_organic_soils_area_ha)}
            · CO₂: ${fmtKt(r.co2_kt_co2)}
            · N₂O: ${fmtKt(r.n2o_ar5_kt_co2e)}
          </p>
        </div>
      </article>
    `).join("");
  }

  async function renderHotspots() {
    const root = document.querySelector("#hotspotLayer");
    if (!root) return;

    try {
      const res = await fetch(HOTSPOT_DATA_URL);
      if (!res.ok) throw new Error(`Failed to load ${HOTSPOT_DATA_URL}`);
      const rows = parseCSV(await res.text());
      const complete = completeRows(rows);

      const total = document.querySelector("#hotspotMetricCountries");
      const year = document.querySelector("#hotspotMetricYear");
      const emissions = document.querySelector("#hotspotMetricEmissions");

      if (total) total.textContent = complete.length;
      if (year) year.textContent = complete[0]?.year || "—";
      if (emissions) {
        const sum = complete.reduce((acc, r) => acc + (num(r.emissions_total_kt_co2e) || 0), 0);
        emissions.textContent = `${(sum / 1000).toFixed(1)} Mt CO₂e`;
      }

      const totalEl = document.querySelector("#hotspotRankingTotal");
      const densityEl = document.querySelector("#hotspotRankingDensity");

      if (totalEl) renderRanking(totalEl, complete, "emissions_total_kt_co2e", "Total emissions", fmtKt);
      if (densityEl) renderRanking(densityEl, complete, "emissions_density_t_co2e_per_ha", "Emissions density", fmtDensity);

      root.classList.remove("loading");
    } catch (err) {
      root.innerHTML = `
        <div class="detail-card">
          <p class="eyebrow">Hotspot layer</p>
          <h3>Could not load hotspot data</h3>
          <p>${err.message}</p>
        </div>
      `;
      console.error(err);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderHotspots);
  } else {
    renderHotspots();
  }
})();
