FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY mcp_server.py /app/mcp_server.py
USER 1000:1000
EXPOSE 18765
ENTRYPOINT ["python","/app/mcp_server.py"]
CMD ["--host","0.0.0.0","--port","18765"]

LABEL org.opencontainers.image.source="https://github.com/GodsQuantum/Cloud9-Fincept-MCP" org.opencontainers.image.title="Cloud9-Fincept-MCP" org.opencontainers.image.description="Independent read-only market and factor MCP with synthetic regression tests"
