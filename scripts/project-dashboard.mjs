import { readFileSync, existsSync, statSync } from 'node:fs';
import { resolve, dirname, extname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createServer } from 'node:http';
import { buildSnapshot, project, atomicWrite, markdown } from '../packages/project-status/index.mjs';

const repo = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2), command = args.shift() ?? 'check';
const options = {};
while (args.length) {
  const flag = args.shift();
  if (!['--vault-root','--register','--mode','--port'].includes(flag) || !args.length) throw new Error('Ungültige CLI-Option');
  options[flag.slice(2)] = args.shift();
}
if (!['check','update','build','preview'].includes(command)) throw new Error('Ungültiger Befehl');
const vault = resolve(options['vault-root'] ?? process.env.IUM_VAULT_ROOT ?? resolve(repo,'../../Vault'));
const register = resolve(options.register ?? join(vault,'40_Projekte/IuM-Lernwerk/IuM-Lernwerk Statusregister.md'));
const mode = options.mode ?? 'presentation';
if (!['presentation','internal'].includes(mode)) throw new Error('Ungültiger Modus');
const snapshot = buildSnapshot({repo,vault,register});
const output = resolve(repo,'dist/dashboard');
if (command === 'check') {
  console.log(`Dashboardvertrag gültig: ${snapshot.gates.length} Gates, ${snapshot.streams.length} Stränge, ${snapshot.evidence.length} Belege. ${snapshot.warnings.length} optionale Quellenlücke(n).`);
} else {
  const serialized = JSON.stringify(snapshot,null,2)+'\n';
  // Validate and prepare both projections before any replacement.
  const md = markdown(snapshot);
  const mdPath = join(vault,'40_Projekte/IuM-Lernwerk/IuM-Lernwerk Dashboard.md');
  const previous = existsSync(mdPath) ? readFileSync(mdPath,'utf8') : null;
  if (command === 'update') atomicWrite(mdPath,md);
  try { atomicWrite(join(output,'snapshot.json'),serialized,JSON.parse); }
  catch (error) { if (command === 'update' && previous !== null) atomicWrite(mdPath,previous); throw error; }
  if (command === 'update') console.log('Snapshot und Obsidian-Cockpit aktualisiert.');
  else {
    const stamp = Date.now().toString(), buildDir = join(output,mode,stamp);
    const input = join(output,`input-${mode}-${stamp}.json`);
    atomicWrite(input,JSON.stringify(project(snapshot,mode)));
    process.env.IUM_DASHBOARD_INPUT = input;
    process.env.IUM_DASHBOARD_OUT = buildDir;
    const { build } = await import('astro');
    await build({ root: pathToFileURL(resolve(repo,'apps/project-dashboard')+'/') });
    atomicWrite(join(output,`latest-${mode}.json`),JSON.stringify({directory:relativeOutput(buildDir),head:snapshot.git.head,mode}));
    console.log(`Dashboard gebaut (${mode}).`);
    if (command === 'preview') {
      const port = Number(options.port ?? 4324);
      if (!Number.isInteger(port) || port < 1024 || port > 65535) throw new Error('Ungültiger Port');
      const mime = { '.html':'text/html; charset=utf-8', '.css':'text/css; charset=utf-8', '.svg':'image/svg+xml', '.json':'application/json; charset=utf-8' };
      createServer((req,res) => {
        try {
          if (!['GET','HEAD'].includes(req.method)) { res.writeHead(405).end(); return; }
          const pathname = decodeURIComponent(new URL(req.url,'http://127.0.0.1').pathname);
          if (pathname.includes('..') || pathname.includes('\\')) throw new Error('Ungültiger Pfad');
          let file = join(buildDir,pathname);
          if (existsSync(file) && statSync(file).isDirectory()) file = join(file,'index.html');
          if (!existsSync(file) || !statSync(file).isFile()) { res.writeHead(404).end('Nicht gefunden'); return; }
          res.writeHead(200,{'Content-Type':mime[extname(file)]??'application/octet-stream','Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Content-Security-Policy':"default-src 'none'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'none'; script-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'"});
          res.end(req.method === 'HEAD' ? undefined : readFileSync(file));
        } catch { res.writeHead(400).end('Ungültige Anfrage'); }
      }).listen(port,'127.0.0.1',()=>console.log(`Lokale ${mode === 'presentation'?'Präsentation':'Arbeitsansicht'}: http://127.0.0.1:${port}/`));
    }
  }
}
function relativeOutput(path) { return path.slice(repo.length+1).replaceAll('\\','/'); }
