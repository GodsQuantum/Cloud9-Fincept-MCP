#!/usr/bin/env python3
from pathlib import Path
import subprocess,re,json,xml.etree.ElementTree as ET
base=Path(__file__).resolve().parent.parent
items=subprocess.check_output(["git","-C",str(base),"ls-files","-z"]).decode().split(chr(0))
patterns=[re.compile(s,re.I) for s in ["a"+"rezki","chou"+"gar","kech"+"idi","fe"+"lla",
 r"192[.]168[.]",r"home[.]arpa",r"@gmail[.]com","/srv/"+"lxc/",
 r"-----BEGIN PRIVATE KEY",r"github_pat_[A-Za-z0-9_]{25,}",r"ghp_[a-zA-Z0-9]{25,}"]]
failed=[]
for name in items:
 if not name or name=="tests/privacy.py":continue
 file=base/name
 if not file.is_file() or file.stat().st_size>350000:continue
 if any(p.search(file.read_text(errors="replace")) for p in patterns):failed.append(name)
assert not failed,("PERSONAL_DATA_PUBLICATION_DENIED",failed)
names=json.loads((base/"tests/tool-names.json").read_text())
digests=json.loads((base/"tests/tool-schema-sha256.json").read_text())
assert len(names)==len(set(names))==5 and set(names)==set(digests)
assert all(len(h)==64 for h in digests.values())
ET.parse(base/"docs/logo.svg");ET.parse(base/"docs/tools.svg")
print("FINCEPT_PUBLIC_SOURCE_FIVE_TOOLS_PRIVACY_PASS")
