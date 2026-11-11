#!/bin/sh
set -eu
python /app/mcp_server.py --selftest >/tmp/selftest.log 2>&1 || { tail -50 /tmp/selftest.log;exit 1; }
tail -2 /tmp/selftest.log
python /app/mcp_server.py --host 127.0.0.1 --port 18765 >/tmp/server.log 2>&1 &
server=$!
ready=no
for i in $(seq 1 40);do
 if python -c 'import socket; s=socket.create_connection(("127.0.0.1",18765),timeout=2);s.close()' 2>/dev/null;then
  ready=yes
  break
 fi
 sleep 2
done
if [ "$ready" != yes ];then tail -70 /tmp/server.log;exit 1;fi
python /contract/verify_tools.py || { tail -90 /tmp/server.log;exit 1; }
kill "$server" 2>/dev/null || true
echo FINCEPT_CANDIDATE_REAL_MCP_AND_OFFLINE_REGRESSIONS_PASS
