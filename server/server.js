#!/usr/bin/env node
/* ==========================================================================
   B2B2 Builders — static site server + leads backend
   Zero dependencies (Node 18+). Run:  node server/server.js  (or: npm start)

   - Serves the static site from the repo root (same paths as production).
   - POST /api/lead            — accepts JSON from the 3 site forms, stores it.
   - GET  /admin               — password-gated leads dashboard (password: 0000).
   - Leads persist in server/leads.json (gitignored).
   ========================================================================== */
'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execFile } = require('child_process');

const ROOT = path.resolve(__dirname, '..');

/* ---------- Supabase (leads + calls live in the cloud) ----------
   server/.env is gitignored — the service_role key must never be committed. */
const env = {};
try {
  fs.readFileSync(path.join(__dirname, '.env'), 'utf8').split('\n').forEach((line) => {
    const m = line.match(/^([A-Z_]+)=(.+)$/);
    if (m) env[m[1]] = m[2].trim();
  });
} catch (e) { /* handled below */ }
const SUPABASE_URL = env.SUPABASE_URL;
const SUPABASE_KEY = env.SUPABASE_SERVICE_KEY;
if (!SUPABASE_URL || !SUPABASE_KEY) {
  console.error('Missing server/.env with SUPABASE_URL and SUPABASE_SERVICE_KEY — admin data will not load.');
}

async function supa(pathAndQuery, options) {
  const opts = Object.assign({ method: 'GET' }, options || {});
  opts.headers = Object.assign({
    apikey: SUPABASE_KEY,
    Authorization: `Bearer ${SUPABASE_KEY}`,
    'Content-Type': 'application/json',
    Prefer: 'return=representation'
  }, opts.headers || {});
  if (opts.body && typeof opts.body !== 'string') opts.body = JSON.stringify(opts.body);
  const r = await fetch(`${SUPABASE_URL}/rest/v1/${pathAndQuery}`, opts);
  const text = await r.text();
  const data = text ? JSON.parse(text) : null;
  if (!r.ok) throw new Error(`Supabase ${r.status}: ${text.slice(0, 200)}`);
  return data;
}

/* DB columns are snake_case; the site + admin UI speak camelCase. */
const LEAD_FIELDS = {
  receivedAt: 'received_at', status: 'status', source: 'source', name: 'name',
  phone: 'phone', email: 'email', projectType: 'project_type', projectSize: 'project_size',
  propertyType: 'property_type', ownership: 'ownership', timeline: 'timeline',
  budget: 'budget', location: 'location', zip: 'zip', area: 'area',
  contactPref: 'contact_pref', notes: 'notes', message: 'message', page: 'page'
};
function leadToApi(row) {
  const out = { id: row.id };
  for (const [api, col] of Object.entries(LEAD_FIELDS)) out[api] = row[col];
  return out;
}
function leadToDb(payload) {
  const out = {};
  for (const [api, col] of Object.entries(LEAD_FIELDS)) {
    if (api === 'receivedAt' || api === 'status') continue; // db defaults
    if (typeof payload[api] === 'string') out[col] = payload[api].slice(0, 2000);
  }
  return out;
}
const SECRET_FILE = path.join(__dirname, '.session-secret');
const ADMIN_HTML = path.join(__dirname, 'admin.html');
const PORT = process.env.PORT || 8742;

// TODO: change before real launch — plain password per owner request ("0000 for now")
const ADMIN_PASSWORD = '0000';

/* ---------- session token ---------- */
let secret;
try {
  secret = fs.readFileSync(SECRET_FILE, 'utf8');
} catch (e) {
  secret = crypto.randomBytes(32).toString('hex');
  fs.writeFileSync(SECRET_FILE, secret, { mode: 0o600 });
}
const SESSION_TOKEN = crypto.createHmac('sha256', secret).update(ADMIN_PASSWORD).digest('hex');

function isAuthed(req) {
  const cookies = (req.headers.cookie || '').split(';').map(c => c.trim());
  return cookies.includes('b2b2_admin=' + SESSION_TOKEN);
}

/* ---------- leads store: Supabase (see helpers above) ---------- */
/* ---------- projects store (single source of truth for the site pages) ---------- */
const PROJECTS_FILE = path.join(__dirname, 'projects-data.json');

function readProjects() {
  return JSON.parse(fs.readFileSync(PROJECTS_FILE, 'utf8'));
}
function writeProjects(projects) {
  const tmp = PROJECTS_FILE + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(projects, null, 2));
  fs.renameSync(tmp, PROJECTS_FILE);
}

/* Regenerate the static project pages + hub after a data change.
   Runs the Python generator then the partial injector, serialized so
   concurrent edits can't interleave. */
let regenChain = Promise.resolve();
function regenerate() {
  regenChain = regenChain.then(() => new Promise((resolve) => {
    execFile('python3', ['tools/gen_project_pages.py'], { cwd: ROOT }, (err, out, errOut) => {
      if (err) { console.error('[regen] generator failed:', errOut || err.message); return resolve({ ok: false, error: String(errOut || err.message) }); }
      execFile('python3', ['tools/inject_partials.py'], { cwd: ROOT }, (err2, out2, errOut2) => {
        if (err2) { console.error('[regen] injector failed:', errOut2 || err2.message); return resolve({ ok: false, error: String(errOut2 || err2.message) }); }
        console.log('[regen] project pages regenerated');
        resolve({ ok: true });
      });
    });
  }));
  return regenChain;
}

function run(cmd, args, opts) {
  return new Promise((resolve) => {
    execFile(cmd, args, Object.assign({ cwd: ROOT }, opts), (err, stdout, stderr) => {
      resolve({ ok: !err, stdout: String(stdout || ''), stderr: String(stderr || ''), error: err ? err.message : null });
    });
  });
}

function sanitizeName(name) {
  return name.toLowerCase().replace(/\.[a-z0-9]+$/i, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 60) || 'photo';
}
function altFromName(name) {
  const words = name.replace(/-/g, ' ').trim();
  return words.charAt(0).toUpperCase() + words.slice(1) + ' — B2B2 Builders project photo';
}
function readRawBody(req, maxBytes) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let size = 0;
    req.on('data', (c) => {
      size += c.length;
      if (size > maxBytes) { reject(new Error('too large')); req.destroy(); return; }
      chunks.push(c);
    });
    req.on('end', () => resolve(Buffer.concat(chunks)));
    req.on('error', reject);
  });
}

function callToApi(row) {
  return { id: row.id, clickedAt: row.clicked_at, page: row.page, label: row.label };
}

/* ---------- helpers ---------- */
function send(res, status, body, headers) {
  const h = Object.assign({ 'Content-Type': 'application/json; charset=utf-8' }, headers || {});
  res.writeHead(status, h);
  res.end(typeof body === 'string' ? body : JSON.stringify(body));
}
function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    req.on('data', chunk => {
      data += chunk;
      if (data.length > 1e6) { reject(new Error('too large')); req.destroy(); }
    });
    req.on('end', () => resolve(data));
    req.on('error', reject);
  });
}
function csvEscape(v) {
  const s = v == null ? '' : String(v);
  return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
}

const MIME = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8', '.json': 'application/json',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.webp': 'image/webp', '.avif': 'image/avif', '.gif': 'image/gif',
  '.svg': 'image/svg+xml', '.ico': 'image/x-icon', '.mp4': 'video/mp4',
  '.webm': 'video/webm', '.xml': 'application/xml', '.txt': 'text/plain; charset=utf-8',
  '.woff': 'font/woff', '.woff2': 'font/woff2', '.pdf': 'application/pdf'
};

/* Serve a file with HTTP Range support (needed for the hero video). */
function serveFile(req, res, filePath) {
  fs.stat(filePath, (err, stat) => {
    if (err || !stat.isFile()) return send(res, 404, { error: 'Not found' });
    const ext = path.extname(filePath).toLowerCase();
    const type = MIME[ext] || 'application/octet-stream';
    // Code/content always revalidates; heavy media can cache for a day
    const cache = ['.html', '.css', '.js', '.xml', '.txt', '.json'].includes(ext)
      ? 'no-cache'
      : 'public, max-age=86400';
    res.setHeader('Cache-Control', cache);
    res.setHeader('Last-Modified', stat.mtime.toUTCString());
    const range = req.headers.range;
    if (range) {
      const m = /bytes=(\d*)-(\d*)/.exec(range);
      let start = m && m[1] ? parseInt(m[1], 10) : 0;
      let end = m && m[2] ? parseInt(m[2], 10) : stat.size - 1;
      if (isNaN(start) || start >= stat.size) start = 0;
      if (isNaN(end) || end >= stat.size) end = stat.size - 1;
      res.writeHead(206, {
        'Content-Type': type,
        'Content-Range': `bytes ${start}-${end}/${stat.size}`,
        'Accept-Ranges': 'bytes',
        'Content-Length': end - start + 1
      });
      fs.createReadStream(filePath, { start, end }).pipe(res);
    } else {
      res.writeHead(200, { 'Content-Type': type, 'Content-Length': stat.size, 'Accept-Ranges': 'bytes' });
      fs.createReadStream(filePath).pipe(res);
    }
  });
}

/* ---------- request router ---------- */
const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://localhost');
  const pathname = decodeURIComponent(url.pathname);

  /* ----- public API: accept a lead from any site form ----- */
  if (pathname === '/api/lead' && req.method === 'POST') {
    try {
      const payload = JSON.parse(await readBody(req));
      if (!payload || typeof payload !== 'object') throw new Error('bad payload');
      const row = leadToDb(payload);
      row.page = req.headers.referer || row.page || '';
      const inserted = await supa('leads', { method: 'POST', body: row });
      console.log(`[lead] ${payload.source || 'unknown'} — ${payload.name || ''} ${payload.phone || ''}`);
      return send(res, 200, { ok: true, id: inserted[0] && inserted[0].id });
    } catch (e) {
      console.error('[lead]', e.message);
      return send(res, 400, { ok: false, error: 'Invalid submission' });
    }
  }

  /* ----- public API: log a call-button click ----- */
  if (pathname === '/api/call' && req.method === 'POST') {
    try {
      const payload = JSON.parse(await readBody(req));
      await supa('calls', {
        method: 'POST',
        body: {
          page: typeof payload.page === 'string' ? payload.page.slice(0, 200) : '',
          label: typeof payload.label === 'string' ? payload.label.slice(0, 60) : ''
        }
      });
      return send(res, 200, { ok: true });
    } catch (e) {
      console.error('[call]', e.message);
      return send(res, 400, { ok: false, error: 'Invalid payload' });
    }
  }

  /* ----- admin auth ----- */
  if (pathname === '/api/admin/login' && req.method === 'POST') {
    try {
      const { password } = JSON.parse(await readBody(req));
      if (password === ADMIN_PASSWORD) {
        return send(res, 200, { ok: true }, {
          'Set-Cookie': `b2b2_admin=${SESSION_TOKEN}; Path=/; HttpOnly; SameSite=Strict; Max-Age=604800`
        });
      }
      return send(res, 401, { ok: false, error: 'Wrong password' });
    } catch (e) {
      return send(res, 400, { ok: false, error: 'Bad request' });
    }
  }
  if (pathname === '/api/admin/logout' && req.method === 'POST') {
    return send(res, 200, { ok: true }, {
      'Set-Cookie': 'b2b2_admin=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0'
    });
  }

  /* ----- admin API (auth required) ----- */
  if (pathname.startsWith('/api/admin/') && pathname !== '/api/admin/login') {
    if (!isAuthed(req)) return send(res, 401, { ok: false, error: 'Unauthorized' });

    if (pathname === '/api/admin/leads' && req.method === 'GET') {
      try {
        const rows = await supa('leads?select=*&order=received_at.desc&limit=2000');
        return send(res, 200, { ok: true, leads: rows.map(leadToApi) });
      } catch (e) {
        console.error('[admin/leads]', e.message);
        return send(res, 500, { ok: false, error: 'Supabase unreachable — check server/.env' });
      }
    }
    if (pathname === '/api/admin/calls' && req.method === 'GET') {
      try {
        const rows = await supa('calls?select=*&order=clicked_at.desc&limit=5000');
        return send(res, 200, { ok: true, calls: rows.map(callToApi) });
      } catch (e) {
        console.error('[admin/calls]', e.message);
        return send(res, 500, { ok: false, error: 'Supabase unreachable — check server/.env' });
      }
    }
    if (pathname === '/api/admin/export.csv' && req.method === 'GET') {
      const leads = (await supa('leads?select=*&order=received_at.desc&limit=10000')).map(leadToApi);
      const cols = ['receivedAt', 'source', 'status', 'name', 'phone', 'email', 'projectType',
        'projectSize', 'propertyType', 'ownership', 'timeline', 'budget', 'location', 'zip',
        'area', 'contactPref', 'notes', 'message', 'page'];
      const rows = [cols.join(',')].concat(leads.map(l => cols.map(c => csvEscape(l[c])).join(',')));
      return send(res, 200, rows.join('\n'), {
        'Content-Type': 'text/csv; charset=utf-8',
        'Content-Disposition': 'attachment; filename="b2b2-leads.csv"'
      });
    }
    /* ----- projects management ----- */
    if (pathname === '/api/admin/projects' && req.method === 'GET') {
      const projects = readProjects().map(p => ({
        slug: p.slug,
        title: p.title,
        area: p.area,
        type: p.type,
        category: p.categories[0],
        card: (p.card_img || p.hero_img)[0],
        mediaCount: p.gallery.length + 1
      }));
      return send(res, 200, { ok: true, projects });
    }
    if (pathname === '/api/admin/projects/reorder' && req.method === 'POST') {
      try {
        const { slugs } = JSON.parse(await readBody(req));
        const projects = readProjects();
        const bySlug = {};
        projects.forEach(p => { bySlug[p.slug] = p; });
        if (!Array.isArray(slugs) || slugs.length !== projects.length || slugs.some(s => !bySlug[s])) {
          return send(res, 400, { ok: false, error: 'Slug list mismatch' });
        }
        writeProjects(slugs.map(s => bySlug[s]));
        regenerate();
        return send(res, 200, { ok: true });
      } catch (e) {
        return send(res, 400, { ok: false, error: 'Bad request' });
      }
    }
    const projMatch = pathname.match(/^\/api\/admin\/projects\/([a-z0-9-]+)(\/featured|\/media)?$/);
    if (projMatch) {
      const projects = readProjects();
      const proj = projects.find(p => p.slug === projMatch[1]);
      if (!proj) return send(res, 404, { ok: false, error: 'Unknown project' });

      if (!projMatch[2] && req.method === 'GET') {
        return send(res, 200, { ok: true, project: proj });
      }

      if (projMatch[2] === '/featured' && req.method === 'POST') {
        try {
          const { src } = JSON.parse(await readBody(req));
          const all = [proj.hero_img].concat(proj.gallery);
          const hit = all.find(item => !Array.isArray(item) ? item.poster === src : item[0] === src);
          if (!hit) return send(res, 400, { ok: false, error: 'Image not in this project' });
          proj.card_img = Array.isArray(hit) ? [hit[0], hit[1]] : [hit.poster, hit.alt];
          writeProjects(projects);
          regenerate();
          return send(res, 200, { ok: true, card_img: proj.card_img });
        } catch (e) {
          return send(res, 400, { ok: false, error: 'Bad request' });
        }
      }

      if (projMatch[2] === '/media' && req.method === 'POST') {
        try {
          const rawName = decodeURIComponent(url.searchParams.get('filename') || 'photo.jpg');
          const ext = (rawName.match(/\.([a-z0-9]+)$/i) || [, ''])[1].toLowerCase();
          const base = sanitizeName(rawName);
          const dir = path.join(ROOT, 'Images', 'projects', proj.slug);
          fs.mkdirSync(dir, { recursive: true });
          const body = await readRawBody(req, 300e6);

          if (['jpg', 'jpeg', 'png', 'heic', 'webp'].includes(ext)) {
            const tmp = path.join(dir, `.upload-tmp.${ext}`);
            fs.writeFileSync(tmp, body);
            const dest = path.join(dir, `${base}.jpg`);
            const r = await run('sips', ['-s', 'format', 'jpeg', '-s', 'formatOptions', '75', '-Z', '1600', tmp, '--out', dest]);
            fs.unlinkSync(tmp);
            if (!r.ok || !fs.existsSync(dest)) return send(res, 400, { ok: false, error: 'Image conversion failed' });
            proj.gallery.push([`/Images/projects/${proj.slug}/${base}.jpg`, altFromName(base)]);
          } else if (['mp4', 'mov'].includes(ext)) {
            let dest = path.join(dir, `${base}.mp4`);
            if (ext === 'mov') {
              const tmp = path.join(dir, `.upload-tmp.mov`);
              fs.writeFileSync(tmp, body);
              const r = await run('avconvert', ['-p', 'Preset1280x720', '-s', tmp, '-o', dest]);
              fs.unlinkSync(tmp);
              if (!r.ok) return send(res, 400, { ok: false, error: 'Video conversion failed' });
            } else {
              fs.writeFileSync(dest, body);
            }
            // Poster frame via Quick Look, then resize to jpg
            const posterPath = path.join(dir, `${base}-poster.jpg`);
            const thumbDir = fs.mkdtempSync(path.join(require('os').tmpdir(), 'b2b2-thumb-'));
            await run('qlmanage', ['-t', '-s', '1200', '-o', thumbDir, dest]);
            const thumb = fs.readdirSync(thumbDir).find(n => n.endsWith('.png'));
            if (thumb) {
              await run('sips', ['-s', 'format', 'jpeg', '-s', 'formatOptions', '75', path.join(thumbDir, thumb), '--out', posterPath]);
            }
            fs.rmSync(thumbDir, { recursive: true, force: true });
            proj.gallery.push({
              video: `/Images/projects/${proj.slug}/${base}.mp4`,
              poster: fs.existsSync(posterPath) ? `/Images/projects/${proj.slug}/${base}-poster.jpg` : '',
              alt: altFromName(base)
            });
          } else {
            return send(res, 400, { ok: false, error: 'Use jpg, png, heic, webp, mp4, or mov' });
          }
          writeProjects(projects);
          regenerate();
          return send(res, 200, { ok: true, gallery: proj.gallery });
        } catch (e) {
          console.error('[upload]', e);
          return send(res, 400, { ok: false, error: 'Upload failed: ' + e.message });
        }
      }
    }

    if (pathname === '/api/admin/publish' && req.method === 'POST') {
      await regenChain; // let any pending regeneration finish first
      const status = await run('git', ['status', '--porcelain']);
      if (!status.stdout.trim()) return send(res, 200, { ok: true, message: 'Nothing to publish — live site is up to date.' });
      await run('git', ['add', '-A']);
      const commit = await run('git', ['commit', '-m', 'Content update from admin dashboard']);
      if (!commit.ok) return send(res, 500, { ok: false, error: 'Commit failed: ' + commit.stderr });
      const push = await run('git', ['push', 'origin', 'main']);
      if (!push.ok) return send(res, 500, { ok: false, error: 'Push failed: ' + push.stderr });
      return send(res, 200, { ok: true, message: 'Published — Vercel is deploying the update now (live in ~1 minute).' });
    }

    const leadMatch = pathname.match(/^\/api\/admin\/leads\/([a-f0-9-]+)$/);
    if (leadMatch) {
      const id = encodeURIComponent(leadMatch[1]);
      if (req.method === 'PATCH') {
        try {
          const { status } = JSON.parse(await readBody(req));
          if (!['new', 'contacted', 'won', 'archived'].includes(status)) {
            return send(res, 400, { ok: false, error: 'Bad status' });
          }
          const rows = await supa(`leads?id=eq.${id}`, { method: 'PATCH', body: { status } });
          if (!rows.length) return send(res, 404, { ok: false, error: 'Not found' });
          return send(res, 200, { ok: true, lead: leadToApi(rows[0]) });
        } catch (e) {
          return send(res, 400, { ok: false, error: 'Bad request' });
        }
      }
      if (req.method === 'DELETE') {
        try {
          await supa(`leads?id=eq.${id}`, { method: 'DELETE' });
          return send(res, 200, { ok: true });
        } catch (e) {
          return send(res, 500, { ok: false, error: 'Delete failed' });
        }
      }
    }
    return send(res, 404, { ok: false, error: 'Not found' });
  }

  /* ----- admin UI ----- */
  if (pathname === '/admin' || pathname === '/admin/') {
    return serveFile(req, res, ADMIN_HTML);
  }

  /* ----- static site ----- */
  if (req.method !== 'GET' && req.method !== 'HEAD') return send(res, 405, { error: 'Method not allowed' });
  // Never serve the server's own directory or hidden files
  if (pathname.startsWith('/server/') || pathname.split('/').some(seg => seg.startsWith('.'))) {
    return send(res, 404, { error: 'Not found' });
  }
  let filePath = path.normalize(path.join(ROOT, pathname));
  if (!filePath.startsWith(ROOT)) return send(res, 403, { error: 'Forbidden' });
  if (pathname.endsWith('/')) filePath = path.join(filePath, 'index.html');
  fs.stat(filePath, (err, stat) => {
    if (!err && stat.isDirectory()) {
      // /projects → redirect to /projects/ so relative paths resolve
      res.writeHead(301, { Location: pathname + '/' });
      return res.end();
    }
    serveFile(req, res, filePath);
  });
});

server.listen(PORT, () => {
  console.log(`B2B2 Builders site + leads backend running:`);
  console.log(`  Site:  http://localhost:${PORT}/`);
  console.log(`  Admin: http://localhost:${PORT}/admin  (password: ${ADMIN_PASSWORD})`);
});
