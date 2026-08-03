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

const ROOT = path.resolve(__dirname, '..');
const DATA_FILE = path.join(__dirname, 'leads.json');
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

/* ---------- leads store ---------- */
function readLeads() {
  try {
    return JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
  } catch (e) {
    return [];
  }
}
function writeLeads(leads) {
  const tmp = DATA_FILE + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(leads, null, 2));
  fs.renameSync(tmp, DATA_FILE);
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
      const lead = Object.assign({}, payload, {
        id: crypto.randomUUID(),
        receivedAt: new Date().toISOString(),
        status: 'new',
        page: req.headers.referer || ''
      });
      const leads = readLeads();
      leads.unshift(lead);
      writeLeads(leads);
      console.log(`[lead] ${lead.receivedAt} ${lead.source || 'unknown'} — ${lead.name || ''} ${lead.phone || ''}`);
      return send(res, 200, { ok: true, id: lead.id });
    } catch (e) {
      return send(res, 400, { ok: false, error: 'Invalid submission' });
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
      return send(res, 200, { ok: true, leads: readLeads() });
    }
    if (pathname === '/api/admin/export.csv' && req.method === 'GET') {
      const leads = readLeads();
      const cols = ['receivedAt', 'source', 'status', 'name', 'phone', 'email', 'projectType',
        'projectSize', 'propertyType', 'ownership', 'timeline', 'budget', 'location', 'zip',
        'area', 'contactPref', 'notes', 'message', 'page'];
      const rows = [cols.join(',')].concat(leads.map(l => cols.map(c => csvEscape(l[c])).join(',')));
      return send(res, 200, rows.join('\n'), {
        'Content-Type': 'text/csv; charset=utf-8',
        'Content-Disposition': 'attachment; filename="b2b2-leads.csv"'
      });
    }
    const leadMatch = pathname.match(/^\/api\/admin\/leads\/([a-f0-9-]+)$/);
    if (leadMatch) {
      const leads = readLeads();
      const idx = leads.findIndex(l => l.id === leadMatch[1]);
      if (idx === -1) return send(res, 404, { ok: false, error: 'Not found' });
      if (req.method === 'PATCH') {
        try {
          const { status } = JSON.parse(await readBody(req));
          if (['new', 'contacted', 'won', 'archived'].includes(status)) {
            leads[idx].status = status;
            writeLeads(leads);
            return send(res, 200, { ok: true, lead: leads[idx] });
          }
          return send(res, 400, { ok: false, error: 'Bad status' });
        } catch (e) {
          return send(res, 400, { ok: false, error: 'Bad request' });
        }
      }
      if (req.method === 'DELETE') {
        leads.splice(idx, 1);
        writeLeads(leads);
        return send(res, 200, { ok: true });
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
