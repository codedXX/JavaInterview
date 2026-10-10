import json

with open(r'F:\Projects\JavaInterview\preview_rows.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

extracted = []
for item in data.get('rows', []):
    vals = item.get('vals', [])
    if len(vals) >= 4:
        pid = vals[2].strip()
        name = vals[3].strip()
        if pid and pid != "" and pid != "None":
            clean_name = " ".join(name.split())
            extracted.append({
                "productId": pid,
                "productName": clean_name
            })

with open(r'F:\Projects\JavaInterview\extracted_products.json', 'w', encoding='utf-8') as f:
    json.dump(extracted, f, ensure_ascii=False, indent=2)
