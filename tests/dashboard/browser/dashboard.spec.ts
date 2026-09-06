import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { resolve, join } from 'node:path';

const routes = ['','baselines','foundations','experience','audit','grades','gates','evidence'];
test('all eight views and every local link resolve; no background network outside localhost',async({page,request})=>{
  const unexpected:string[]=[];
  page.on('request',r=>{if(!r.url().startsWith(`http://127.0.0.1:${process.env.IUM_DASHBOARD_TEST_PORT ?? '4324'}/`))unexpected.push(r.url());});
  const links=new Set<string>();
  for(const route of routes){
    await page.goto('/'+route);
    await expect(page.locator('h1')).toHaveCount(1);
    await expect(page.locator('nav a')).toHaveCount(8);
    await expect(page.locator('script')).toHaveCount(0);
    for(const href of await page.locator('a').evaluateAll(as=>as.map(a=>(a as HTMLAnchorElement).getAttribute('href')!))){if(href.startsWith('/'))links.add(href.split('#')[0]);}
  }
  for(const link of links){expect((await request.get(link)).status(),link).toBe(200);}
  expect(unexpected).toEqual([]);
  expect((await request.get('/evidence/internal-review/')).status()).toBe(404);
  await page.goto('/gates/');
  await expect(page.getByRole('heading',{name:'V2 als Planungs- und Entwicklungsbaseline aktiviert'})).toBeVisible();
  await expect(page.locator('#cutover-options')).toHaveCount(0);
  await expect(page.locator('.gate-list .badge')).toHaveCount(18);
  await expect(page.locator('.gate-list .badge').last()).toHaveText(/Freigegeben|In Arbeit/);
  await page.goto('/baselines/');await expect(page.getByRole('heading',{name:'Planungsbaseline · aktiv'})).toBeVisible();
});
test('all views meet automated WCAG 2.2 AA checks',async({page})=>{
  for(const route of routes){await page.goto('/'+route);const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze();expect(result.violations,route).toEqual([]);}
});
test('keyboard skip link and navigation work',async({page})=>{
  await page.goto('/');await page.keyboard.press('Tab');await expect(page.getByRole('link',{name:'Zum Inhalt'})).toBeFocused();await page.keyboard.press('Enter');await expect(page.locator('main')).toBeFocused();
  await page.locator('nav a[href="/grades/"]').focus();
  await page.keyboard.press('Enter');await expect(page).toHaveURL(/\/grades\//);
  await expect(page.getByRole('heading',{name:'Klasse 7: Bedarf ist keine Verfügbarkeit'})).toBeVisible();
});
test('phone and tablet do not overflow; uncertainty remains visible',async({page})=>{
  for(const width of [390,768]){await page.setViewportSize({width,height:900});for(const route of routes){await page.goto('/'+route);expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${width} ${route}`).toBe(true);}}
  await page.goto('/grades/');await expect(page.getByRole('heading',{name:'Neun unterschiedliche Nachweisfragen'})).toBeVisible();
  await page.screenshot({path:'reports/dashboard-mobile.png',fullPage:true});
});
test('print includes all gates and all maturity columns; no navigation ink',async({page})=>{
  await page.emulateMedia({media:'print'});await page.goto('/gates/');await expect(page.locator('.sidebar')).toBeHidden();await expect(page.locator('.gate-list li')).toHaveCount(18);
  await page.pdf({path:'reports/dashboard-gates.pdf',format:'A4',printBackground:true});
  await page.goto('/foundations/');await expect(page.locator('#print-maturity thead th')).toHaveCount(6);await expect(page.locator('#print-maturity tbody tr')).toHaveCount(8);
  expect(await page.evaluate(()=>document.querySelector('#print-maturity table')!.scrollWidth<=document.querySelector('main')!.clientWidth)).toBe(true);
  await page.pdf({path:'reports/dashboard-maturity.pdf',format:'A4',printBackground:true});
});
test('built presentation contains no internal evidence, local absolute paths or active external resources',async({page})=>{
  const manifest=JSON.parse(readFileSync('dist/dashboard/latest-presentation.json','utf8'));
  const root=resolve(manifest.directory);
  const files=(dir:string):string[]=>readdirSync(dir).flatMap(n=>statSync(join(dir,n)).isDirectory()?files(join(dir,n)):[join(dir,n)]);
  for(const file of files(root)){
    const text=readFileSync(file,'utf8');expect(text,file).not.toMatch(/internal-review|Interner Prüfsnapshot R7|C:(?:\\|\/)|file:\/\/|src=["']https?:\/\//);
  }
  await page.goto('/');await page.screenshot({path:'reports/dashboard-desktop.png',fullPage:true});
});
