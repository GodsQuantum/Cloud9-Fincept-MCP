#!/usr/bin/env python3
import asyncio,hashlib,json
from pathlib import Path
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
async def main():
 expected=set(json.loads(Path("/contract/tool-names.json").read_text()))
 digests=json.loads(Path("/contract/tool-schema-sha256.json").read_text())
 async with streamable_http_client("http://127.0.0.1:18765/mcp") as channel:
  async with ClientSession(channel[0],channel[1]) as session:
   await session.initialize()
   tools=(await session.list_tools()).tools
   names={v.name for v in tools}
   assert names==expected,("FIVE_TOOL_REGRESSION",sorted(expected-names),sorted(names-expected))
   modified=[]
   for v in tools:
    content=json.dumps(v.input_schema,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    if hashlib.sha256(content).hexdigest()!=digests[v.name]:modified.append(v.name)
   assert not modified,("INPUT_SCHEMA_CHANGED",modified)
   print("FINCEPT_5_TOOLS_INPUT_SCHEMAS_IDENTICAL",flush=True)
asyncio.run(main())
