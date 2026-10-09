const fs = require('node:fs/promises');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('C:/Users/YX/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async () => {
  const out = __dirname;
  const browser = await chromium.launch({ headless: true, executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe' });
  try {
    const page = await browser.newPage({ viewport: { width: 1250, height: 900 }, deviceScaleFactor: 1.5 });
    await page.goto(pathToFileURL(path.join(out, '企业文化墙报价_打印版.html')).href);
    await page.evaluate(() => Promise.all(Array.from(document.images, image => image.decode())));
    await page.emulateMedia({ media: 'print' });
    const geometry = await page.evaluate(() => {
      const rect = el => { const r = el.getBoundingClientRect(); return { x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom }; };
      return { sheet: rect(document.querySelector('.sheet')), table: rect(document.querySelector('table')), note: rect(document.querySelector('.note')), image: rect(document.querySelector('img')), toolbarDisplay: getComputedStyle(document.querySelector('.toolbar')).display, text: document.querySelector('.sheet').innerText };
    });
    await fs.writeFile(path.join(out, 'support', 'print-geometry.json'), JSON.stringify(geometry, null, 2));
    await page.pdf({ path: path.join(out, '企业文化墙报价_打印版.pdf'), preferCSSPageSize: true, printBackground: true, displayHeaderFooter: false });
    await page.locator('.sheet').screenshot({ path: path.join(out, 'support', 'html-print-preview.png') });
    console.log(JSON.stringify(geometry));
  } finally { await browser.close(); }
})().catch(e => { console.error(e); process.exitCode = 1; });

