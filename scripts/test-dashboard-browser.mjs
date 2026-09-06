import { spawn } from 'node:child_process';
const server = spawn(process.execPath,['scripts/project-dashboard.mjs','preview'],{stdio:['ignore','pipe','inherit']});
try {
  await new Promise((resolve,reject)=>{
    let output='';
    const timeout=setTimeout(()=>reject(new Error('Dashboard-Start überschreitet 120 Sekunden')),120_000);
    server.stdout.on('data',chunk=>{output+=chunk; if(output.includes('http://127.0.0.1:4324/')){clearTimeout(timeout);resolve();}});
    server.once('error',error=>{clearTimeout(timeout);reject(error);});
    server.once('exit',code=>{clearTimeout(timeout);reject(new Error(`Dashboard vorzeitig beendet: ${code}`));});
  });
  const test = spawn(process.execPath,['node_modules/@playwright/test/cli.js','test','--config','playwright.dashboard.config.mts'],{stdio:'inherit',env:{...process.env,IUM_DASHBOARD_TEST_SERVER:'owned'}});
  process.exitCode = await new Promise((resolve,reject)=>{test.once('exit',code=>resolve(code??1));test.once('error',reject);});
} finally { server.kill(); }
