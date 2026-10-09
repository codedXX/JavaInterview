import json,pathlib,collections,pdfplumber,pypdfium2
from PIL import Image,ImageDraw
root=pathlib.Path('F:/Projects/JavaInterview')
file=root/'12-押题/新邓懿轩-面试押题.pdf'
out=root/'tmp/pdfs/deng/qa';out.mkdir(exist_ok=True)
pdf=pdfplumber.open(file)
print('pages',len(pdf.pages),'metadata',pdf.metadata)
print('first-page',pdf.pages[0].extract_text()[:1500])
print('font counts',collections.Counter((c['fontname'],round(c['size'],2)) for p in pdf.pages for c in p.chars).most_common(12))
terms=['RRF','余弦相似度','点积','xrightarrow','Function Calling','最终，这个结构','正确写法（栈封闭','Trace','Trace ID','userRagDocs']
loc={s:[] for s in terms}
for i,page in enumerate(pdf.pages):
 t=page.extract_text() or ''
 for s in terms:
  if s in t:loc[s].append(i+1)
print('locations',json.dumps(loc,ensure_ascii=False))
selected={0,1,2,len(pdf.pages)-1}
for t,ls in loc.items():
 if ls:selected.add(ls[0]-1)
selected.update(range(max(0,len(pdf.pages)-5),len(pdf.pages)))
doc=pypdfium2.PdfDocument(str(file))
for i in sorted(selected):doc[i].render(scale=1.6).to_pil().save(out/f'page-{i+1:03}.png')
for start in range(0,len(doc),12):
 sheet=Image.new('RGB',(1200,1740),'#e5e5e5');draw=ImageDraw.Draw(sheet)
 for n,i in enumerate(range(start,min(start+12,len(doc)))):
  image=doc[i].render(scale=.6).to_pil();image.thumbnail((290,405));x=(n%4)*300+(300-image.width)//2;y=(n//4)*580+28
  sheet.paste(image,(x,y));draw.text((x,y-18),f'Page {i+1}',fill='black')
 sheet.save(out/f'contact-{start//12+1:02}.png')
print('rendered',len(selected),'sample pages', (len(doc)+11)//12,'contact sheets')
