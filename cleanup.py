import os
import glob

files = glob.glob(r'F:\Projects\JavaInterview\*')
for f in files:
    if any(f.endswith(ext) for ext in ['.py', '.ps1', '.js', '.txt']) and not f.endswith('products.json'):
        try:
            os.remove(f)
        except:
            pass
