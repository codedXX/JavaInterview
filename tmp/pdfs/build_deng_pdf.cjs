const fs = require('fs');
const path = require('path');
const {pathToFileURL} = require('url');
const deps='C:/Users/YX/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/';
const {marked}=require(deps+'marked');
const {chromium}=require(deps+'playwright');
const root='F:/Projects/JavaInterview';
const source=path.join(root,'12-押题/邓懿轩-面试押题.md');
const output=path.join(root,'12-押题/新邓懿轩-面试押题.pdf');
const temp=path.join(root,'tmp/pdfs/deng');
fs.mkdirSync(temp,{recursive:true});
const archive=fs.readFileSync('F:/Typora/resources/lib.asar');
const headerSize=archive.readUInt32LE(4);
const header=JSON.parse(archive.subarray(16,16+archive.readUInt32LE(12)).toString());
const entry=header.files.MathJax3.files.es5.files['tex-svg-full.js'];
const offset=8+headerSize+Number(entry.offset);
fs.writeFileSync(path.join(temp,'tex-svg-full.js'),archive.subarray(offset,offset+entry.size));
const math=[];
function mathHtml(tex,display){const i=math.push({tex,display})-1;return display?`<div class="math-block" data-math="${i}"></div>\n`:`<span class="math-inline" data-math="${i}"></span>`;}
marked.use({extensions:[
{name:'displayMath',level:'block',start(src){const m=src.match(/\$\$|\\\[/);return m?.index;},tokenizer(src){const m=src.match(/^(?:\$\$\s*\n?([\s\S]+?)\$\$|\\\[\s*\n?([\s\S]+?)\\\])(?:\s*\n|$)/);if(m)return{type:'displayMath',raw:m[0],text:m[1]||m[2]};},renderer(t){return mathHtml(t.text.trim(),true);}},
{name:'inlineMath',level:'inline',start(src){const m=src.match(/\$|\\\(/);return m?.index;},tokenizer(src){const m=src.match(/^(?:\$(?!\$)([^\n$]+?)\$|\\\(([^\n]+?)\\\))/);if(m)return{type:'inlineMath',raw:m[0],text:m[1]||m[2]};},renderer(t){return mathHtml(t.text,false);}}
]});
const escape=t=>t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const codeBlocks=[];
marked.use({renderer:{code({text,lang}){text=text.replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&');codeBlocks.push({lang:lang||'',text});return `<pre class="md-fences"><code>${escape(text)}</code></pre>\n`;}}});
const markdown=fs.readFileSync(source,'utf8');
marked.use({tokenizer:{del(){return;}}});
const content=marked.parse(markdown,{gfm:true,breaks:false});
const base=fs.readFileSync('F:/Typora/resources/style/base.css','utf8');
const theme=fs.readFileSync('C:/Users/YX/AppData/Roaming/Typora/themes/github.css','utf8').replace(/@include-when-export[^;]+;/g,'').replaceAll("url('./github/","url('file:///C:/Users/YX/AppData/Roaming/Typora/themes/github/");
const css=`
@page{size:A4;margin:29pt 77.02pt;}
html{font-size:13px;}
body.typora-export{padding:0;border:0;height:auto;}
#write{padding:0;max-width:none;}
#write>h1:first-child{margin-top:38px;}
body{font-family:'Open Sans','Microsoft YaHei',Arial,'Segoe UI Emoji',sans-serif;}
p{orphans:2;widows:2;}
h1,h2,h3,h4,h5,h6{break-after:avoid-page;break-inside:avoid-page;}
blockquote{break-inside:auto;}
table{table-layout:auto;width:100%;overflow:visible;}
th,td{overflow-wrap:anywhere;}
thead{display:table-header-group;}
tr{break-inside:avoid-page;}
a{text-decoration:none;overflow-wrap:anywhere;}
.md-fences{white-space:pre-wrap;overflow-wrap:anywhere;break-inside:avoid-page;line-height:1.6;}
.md-fences code{border:none;padding:0;background:none;font-size:inherit;}
#write pre.diagram{white-space:pre;overflow-wrap:normal;break-inside:avoid-page;}
.math-inline{display:inline;}
.math-block{margin:.8em 0;text-align:center;break-inside:avoid-page;}
.math-block mjx-container{max-width:100%;}
mjx-container{color:inherit;} mjx-assistive-mml{position:absolute!important;width:1px!important;height:1px!important;overflow:hidden!important;clip:rect(1px,1px,1px,1px)!important;}
mjx-container svg{max-width:100%;height:auto;}
`;
const htmlFile=path.join(temp,'document.html');
fs.writeFileSync(htmlFile,`<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>邓懿轩 · 面试押题</title><style>${base}\n${theme}\n${css}</style><script>window.MathJax={startup:{typeset:false},svg:{fontCache:'none'},tex:{packages:{'[+]':['ams','textmacros']}}};</script><script src="tex-svg-full.js"></script></head><body class="typora-export"><div id="write">${content}</div></body></html>`);
(async()=>{
const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
try{
const page=await browser.newPage({viewport:{width:794,height:1123}});
const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto(pathToFileURL(htmlFile).href);
await page.evaluate(async math=>{await MathJax.startup.promise;MathJax.startup.document.addStyleSheet();for(const item of document.querySelectorAll('[data-math]')){const value=math[Number(item.dataset.math)];item.appendChild(await MathJax.tex2svgPromise(value.tex,{display:value.display,em:13,ex:6.5,containerWidth:588}));}await document.fonts.ready;},math);
await page.emulateMedia({media:'print'}); await page.setViewportSize({width:588,height:1045});
const layout=await page.evaluate(()=>{
for(const pre of document.querySelectorAll('pre'))if(/[┌┐└┘│├┤─]/.test(pre.textContent)){pre.classList.add('diagram');let size=parseFloat(getComputedStyle(pre).fontSize);while(pre.scrollWidth>pre.clientWidth+1&&size>6){size-=.2;pre.style.fontSize=size+'px';}}
const write=document.querySelector('#write'),b=write.getBoundingClientRect();
const overflow=[...write.querySelectorAll('p,table,pre,mjx-container')].filter(el=>{const r=el.getBoundingClientRect();return r.right>b.right+1||r.left<b.left-1;}).map(el=>({tag:el.tagName,text:el.textContent.slice(0,100),width:el.getBoundingClientRect().width}));
return{headings:[...write.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h=>h.textContent),tables:write.querySelectorAll('table').length,codes:write.querySelectorAll('pre').length,maths:write.querySelectorAll('[data-math]').length,mathErrors:[...write.querySelectorAll('[data-mml-node="merror"]')].map(e=>e.textContent),overflow,fonts:document.fonts.status,tail:write.textContent.slice(-500)};});
await page.pdf({path:output,preferCSSPageSize:true,printBackground:true,displayHeaderFooter:false,tagged:true,outline:true});
fs.writeFileSync(path.join(temp,'render_audit.json'),JSON.stringify({source,output,math,codeBlocks,layout,errors},null,2));
console.log(JSON.stringify({output,bytes:fs.statSync(output).size,headings:layout.headings.length,tables:layout.tables,codes:layout.codes,maths:layout.maths,mathErrors:layout.mathErrors,overflow:layout.overflow,errors},null,2));
}finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});



