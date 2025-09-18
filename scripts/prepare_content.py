#!/usr/bin/env python3

import sys
import json
import os.path
import markdown2

from pathlib import Path

def tohtml(val):
        return markdown2.markdown(val, extras=["fenced-code-blocks", "full_yaml_metadata"])

def global_meta():
    all_meta_data = []

    src_dir = 'content-src'

    for root, dirs, files in os.walk(src_dir):
        dirs.sort(reverse=True)
        files.sort(reverse=True)
        if 'meta.json' in files:
            meta_file_path = os.path.join(root, 'meta.json')
            with open(meta_file_path, 'r') as meta_file:
                modified_meta_json = json.loads(meta_file.read())
                modified_meta_json['uri'] = meta_file_path.replace("content-src", ".").replace("/meta.json", "")
                found = False
                for i in all_meta_data:
                    if i['uri'] == modified_meta_json['uri']:
                        i = modified_meta_json
                        found = True
                        break

                if found == False:
                    if isinstance(modified_meta_json, dict) and modified_meta_json:  # Ensure the content is a non-empty dictionary
                        all_meta_data.append(modified_meta_json)
                    else:
                        print(f"Warning: {meta_file_path} is empty or not a dictionary.")
    sorted_meta_data = sorted(all_meta_data, key=lambda x: x['date'], reverse=True)
    return json.dumps(sorted_meta_data, sort_keys=True, indent=4, ensure_ascii=False)

def local_meta():
    all_meta_data = []

    src_dir = 'content-src'

    for root, dirs, files in os.walk(src_dir):
        dirs.sort(reverse=True)
        files.sort(reverse=True)
        if 'meta.json' in files:
            meta_file_path = os.path.join(root, 'meta.json')
            with open(meta_file_path, 'r') as meta_file:
                modified_meta_json = json.loads(meta_file.read())
                out_local_path = Path(meta_file_path.replace("content-src", "content"))
                out_local_path.parent.mkdir(parents=True, exist_ok=True)
                with out_local_path.open("w", encoding="utf-8") as f:
                    json.dump(modified_meta_json, f, ensure_ascii=False, separators=(",", ":"))

def local_html():
    all_meta_data = []

    src_dir = 'content-src'

    for root, dirs, files in os.walk(src_dir):
        dirs.sort(reverse=True)
        files.sort(reverse=True)
        if 'gaming-post.md' in files:
            md_file_path = os.path.join(root, 'gaming-post.md')
            with open(md_file_path, "r", encoding="utf-8") as md_file:
                modified_md = md_file.read()
                html = tohtml(modified_md)
                out_local_path = Path(md_file_path.replace("content-src", "content").replace(".md", ".html"))
                out_local_path.parent.mkdir(parents=True, exist_ok=True)
                with out_local_path.open("w", encoding="utf-8") as out_file:
                    out_file.write(html)

result = global_meta()

data = json.loads(result)

# Crée le dossier de sortie si absent
out_path = Path("content/global_meta.json")
out_path.parent.mkdir(parents=True, exist_ok=True)

with out_path.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

local_meta()
local_html()

print(f"Écrit {out_path} ({len(data)} entrées)" if isinstance(data, list) else f"Écrit {out_path}")
