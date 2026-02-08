/* GOVANSH Frontend JS (organized) */

function $(id) { return document.getElementById(id); }

function setTheme(theme) {
  const isLight = theme === 'light';
  document.body.classList.toggle('theme-light', isLight);
  try { localStorage.setItem('govanshTheme', theme); } catch(e) {}
  const btn = $('themeToggle');
  if (btn) btn.textContent = isLight ? 'Dark Mode' : 'Light Mode';
}

function initThemeToggle() {
  let t = 'light';
  try { t = localStorage.getItem('govanshTheme') || 'light'; } catch(e) {}
  setTheme(t);
  const btn = $('themeToggle');
  if (btn) btn.addEventListener('click', () => {
    const next = document.body.classList.contains('theme-light') ? 'dark' : 'light';
    setTheme(next);
  });
}

async function apiJSON(url, opts) {
  const r = await fetch(url, opts);
  const isJSON = (r.headers.get('content-type') || '').includes('application/json');
  const data = isJSON ? await r.json() : null;
  return { ok: r.ok, status: r.status, data };
}

async function loadAuthNav() {
  const nav = $('navAuth');
  if (!nav) return;
  const { ok, data } = await apiJSON('/api/me');
  if (!ok || !data || !data.authenticated) {
    nav.innerHTML = `<a href="/login" style="color:#00d4ff;text-decoration:none;font-weight:800;margin-right:10px;">Login</a>
                     <a href="/signup" style="color:#00ff88;text-decoration:none;font-weight:900;">Sign up</a>`;
    return;
  }
  nav.innerHTML = `<span style="color:#888;margin-right:10px;">Hi, <b style="color:#00ff88;">${data.username}</b></span>
                   <a href="/logout" style="color:#00d4ff;text-decoration:none;font-weight:800;">Logout</a>`;
}

function renderKV(obj, keys) {
  return `<div class="kv">` + keys.map(k => `
    <div><span>${k.label}</span>${obj[k.key] || '-'}</div>
  `).join('') + `</div>`;
}

function renderTop5(top5) {
  return top5.map((p, idx) => {
    const name = p[0];
    const pct = (p[1] * 100).toFixed(1);
    return `<div class="trow" style="grid-template-columns:40px 1fr 120px;">
      <div><b>${idx + 1}</b></div>
      <div>${name}</div>
      <div style="text-align:right;color:#00ff88;font-weight:900;">${pct}%</div>
    </div>`;
  }).join('');
}

async function loadRecent() {
  const el = $('recentList');
  if (!el) return;
  const { ok, data } = await apiJSON('/api/history');
  if (!ok || !data || !data.history || data.history.length === 0) {
    el.innerHTML = 'No predictions yet.';
    return;
  }
  el.innerHTML = data.history.map(h => `
    <div class="recent-item">
      <span>${h.breed} <span class="chip">${h.prediction_id || ''}</span></span>
      <span>${(h.confidence * 100).toFixed(1)}% • ${h.timestamp}</span>
    </div>
  `).join('');
}

async function loadMyPredCount() {
  const el = $('myPred');
  if (!el) return;
  const { ok, data } = await apiJSON('/api/stats');
  if (ok && data) el.textContent = data.my_predictions ?? 0;
}

function downloadReport(lastResult) {
  if (!lastResult) return;
  const info = lastResult.breed_info || {};
  let text = 'GOVANSH - Breed Recognition Report\n';
  text += '================================\n';
  text += `Prediction ID: ${lastResult.prediction_id}\n`;
  text += `Timestamp: ${lastResult.timestamp}\n`;
  text += `Breed: ${lastResult.breed} (${lastResult.hindi_name || ''})\n`;
  text += `Confidence: ${(lastResult.confidence * 100).toFixed(1)}%\n\n`;
  text += `Origin: ${info.origin || ''}\n`;
  text += `Type: ${info.type || ''}\n`;
  text += `Milk Yield: ${info.milk_yield || ''}\n`;
  text += `Market Value: ${info.market_value || ''}\n`;
  text += `Govt Scheme: ${info.govt_scheme || ''}\n`;
  text += `Special: ${info.special || ''}\n`;
  const blob = new Blob([text], { type: 'text/plain' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `govansh_report_${lastResult.prediction_id}.txt`;
  a.click();
  URL.revokeObjectURL(a.href);
}

const GOVANSH = {
  initHome: function () {
    initThemeToggle();
    loadAuthNav();
    loadRecent();
    loadMyPredCount();

    const uploadArea = $('uploadArea');
    const input = $('imageInput');
    const preview = $('preview');
    const previewImg = $('previewImg');
    const analyzeBtn = $('analyzeBtn');
    const loading = $('loading');
    const resultCard = $('resultCard');
    const downloadBtn = $('downloadBtn');

    let currentFile = null;
    let lastResult = null;

    function showTab(name) {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
      document.querySelector(`.tab[data-tab="${name}"]`).classList.add('active');
      $('tab-' + name).classList.add('active');
    }

    document.querySelectorAll('.tab').forEach(t => {
      t.addEventListener('click', () => showTab(t.dataset.tab));
    });

    uploadArea.addEventListener('click', () => input.click());
    uploadArea.addEventListener('dragover', (e) => { e.preventDefault(); uploadArea.style.borderColor = '#00ff88'; });
    uploadArea.addEventListener('dragleave', () => { uploadArea.style.borderColor = ''; });
    uploadArea.addEventListener('drop', (e) => {
      e.preventDefault();
      uploadArea.style.borderColor = '';
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        input.files = e.dataTransfer.files;
        input.dispatchEvent(new Event('change'));
      }
    });

    input.addEventListener('change', () => {
      const f = input.files && input.files[0];
      if (!f) return;
      currentFile = f;
      const reader = new FileReader();
      reader.onload = () => {
        previewImg.src = reader.result;
        preview.style.display = '';
        resultCard.style.display = 'none';
      };
      reader.readAsDataURL(f);
    });

    analyzeBtn.addEventListener('click', async () => {
      loading.style.display = '';
      analyzeBtn.disabled = true;
      resultCard.style.display = 'none';

      const fd = new FormData();
      fd.append('image', currentFile);

      const r = await fetch('/predict', { method: 'POST', body: fd });
      if (r.status === 401) { window.location.href = '/login'; return; }
      const data = await r.json();
      loading.style.display = 'none';
      analyzeBtn.disabled = false;
      if (data.error) { alert(data.error); return; }

      lastResult = data;
      $('breedName').textContent = data.breed || '-';
      $('breedHindi').textContent = data.hindi_name || '';
      $('confVal').textContent = (data.confidence * 100).toFixed(1) + '%';
      $('confVal').style.color = (data.confidence_level && data.confidence_level.color) ? data.confidence_level.color : '';

      const info = data.breed_info || {};
      $('tab-overview').innerHTML = renderKV(info, [
        { key: 'origin', label: 'Origin' },
        { key: 'state', label: 'State' },
        { key: 'type', label: 'Type' },
        { key: 'category', label: 'Category' },
        { key: 'market_value', label: 'Market Value' },
        { key: 'govt_scheme', label: 'Govt Scheme' },
      ]);
      $('tab-details').innerHTML = renderKV(info, [
        { key: 'color', label: 'Color' },
        { key: 'horns', label: 'Horns' },
        { key: 'weight_male', label: 'Weight (Male)' },
        { key: 'weight_female', label: 'Weight (Female)' },
        { key: 'height', label: 'Height' },
        { key: 'lifespan', label: 'Lifespan' },
      ]);
      $('tab-production').innerHTML = renderKV(info, [
        { key: 'milk_yield', label: 'Daily Milk Yield' },
        { key: 'lactation', label: 'Lactation Yield' },
        { key: 'fat_content', label: 'Fat Content' },
        { key: 'gestation', label: 'Gestation' },
        { key: 'first_calving', label: 'First Calving' },
        { key: 'disease_resistance', label: 'Disease Resistance' },
      ]);
      $('tab-care').innerHTML = renderKV(info, [
        { key: 'feeding', label: 'Feeding' },
        { key: 'climate', label: 'Climate' },
        { key: 'special', label: 'Special' },
        { key: 'conservation', label: 'Conservation' },
        { key: 'market_value', label: 'Market Value' },
        { key: 'govt_scheme', label: 'Govt Scheme' },
      ]);
      $('tab-top5').innerHTML = `<div class="table">
        <div class="thead" style="grid-template-columns:40px 1fr 120px;"><div>#</div><div>Breed</div><div style="text-align:right;">Prob</div></div>
        ${renderTop5(data.top_5 || [])}
      </div>`;

      resultCard.style.display = '';
      showTab('overview');
      await loadRecent();
      await loadMyPredCount();
    });

    downloadBtn.addEventListener('click', () => downloadReport(lastResult));
  },

  initCompare: function () {
    initThemeToggle();
    loadAuthNav();
    const btn = $('btnCompare');
    btn.addEventListener('click', async () => {
      const b1 = $('breed1').value;
      const b2 = $('breed2').value;
      if (b1 === b2) { alert('Select two different breeds'); return; }
      const { ok, data } = await apiJSON('/api/compare/' + encodeURIComponent(b1) + '/' + encodeURIComponent(b2));
      if (!ok || data.error) { alert(data.error || 'Compare failed'); return; }
      const panel = (x) => `
        <div class="card">
          <div class="card-title"><span class="icon">🐄</span>${x.name} <span style="color:#fbbf24;font-weight:800;">${x.info.hindi_name||''}</span></div>
          ${renderKV(x.info, [
            {key:'origin',label:'Origin'},
            {key:'type',label:'Type'},
            {key:'milk_yield',label:'Milk Yield'},
            {key:'market_value',label:'Market Value'},
            {key:'climate',label:'Climate'},
            {key:'govt_scheme',label:'Govt Scheme'},
          ])}
        </div>`;
      $('compareGrid').innerHTML = panel(data.breed1) + panel(data.breed2);
    });
  },

  initDashboard: async function () {
    initThemeToggle();
    await loadAuthNav();
    const s = await apiJSON('/api/stats');
    if (s.ok && s.data) {
      $('kMy').textContent = s.data.my_predictions ?? 0;
      $('kUsers').textContent = s.data.total_users ?? 0;
      $('kPred').textContent = s.data.total_predictions ?? 0;
      $('kTop').textContent = (s.data.top_breeds && s.data.top_breeds[0]) ? s.data.top_breeds[0].breed : '-';
      $('topList').innerHTML = (s.data.top_breeds || []).map(t => `
        <div class="mini"><div class="b">${t.breed}</div><div class="c">${t.count} predictions</div></div>
      `).join('') || '<div class="mini">No data yet</div>';
    }
    const h = await apiJSON('/api/history');
    const rows = (h.ok && h.data && h.data.history) ? h.data.history : [];
    $('rows').innerHTML = rows.map(r => `
      <div class="trow"><div>${r.breed} <span class="chip">${r.prediction_id||''}</span></div><div>${(r.confidence*100).toFixed(1)}%</div><div>${r.timestamp}</div></div>
    `).join('') || `<div class="trow"><div>No predictions yet</div><div>-</div><div>-</div></div>`;
  }
};

window.GOVANSH = GOVANSH;

// Always initialize theme + auth on any page
document.addEventListener('DOMContentLoaded', () => {
  initThemeToggle();
  loadAuthNav();
});

