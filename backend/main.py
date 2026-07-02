#!/usr/bin/env python3
"""Dashboard — Backend FastAPI (puerto 8585)"""
import asyncio, json, os, subprocess, sys, urllib.request, urllib.parse, urllib.error
import ssl, re, datetime, time
from pathlib import Path
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

BASE_DIR = Path(__file__).parent.parent
GOOGLE_TOKEN = Path("/root/.hermes/google_token.json")

# ⚠️ Credentials via environment ONLY — never hardcoded
CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
if not CLIENT_ID:
    # Fallback: read from hermes .env
    try:
        with open("/root/.hermes/.env") as f:
            for line in f:
                line = line.strip()
                if line.startswith("GOOGLE_CLIENT_ID="):
                    CLIENT_ID = line.split("=", 1)[1].strip().strip('"').strip("'")
                elif line.startswith("GOOGLE_CLIENT_SECRET="):
                    CLIENT_SECRET = line.split("=", 1)[1].strip().strip('"').strip("'")
    except: pass
TOKEN_URI = "https://oauth2.googleapis.com/token"
NOTAS_DIR = "/var/notas"

def _env_or_empty(key):
    try:
        from hermes_cli.config import get_env_value
        val = get_env_value(key)
        if val: return val
    except: pass
    return os.getenv(key, "")

DEEPSEEK_KEY = _env_or_empty("DEEPSEEK_API_KEY")
if not DEEPSEEK_KEY:
    try:
        with open("/root/.hermes/.env") as f:
            for line in f:
                if line.startswith("DEEPSEEK_API_KEY="):
                    DEEPSEEK_KEY = line.strip().split("=", 1)[1]
                    break
    except: pass

app = FastAPI(title="Dashboard")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def _run(cmd, timeout=10):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip() or r.stderr.strip()
    except: return "ERROR"

def _http(url, timeout=10):
    try:
        ctx = ssl._create_unverified_context()
        r = urllib.request.urlopen(url, timeout=timeout, context=ctx)
        return r.read().decode()
    except: return None

def _get_google_token():
    if not GOOGLE_TOKEN.exists(): return None
    try:
        data = json.loads(GOOGLE_TOKEN.read_text())
        if isinstance(data.get("token"), str): access = data["token"]
        elif isinstance(data.get("token"), dict): access = data["token"].get("access_token", "")
        else: access = data.get("access_token", "")
        if not access: return None
        expiry = data.get("expiry", "")
        if isinstance(data.get("token"), dict): expiry = data["token"].get("expiry", expiry)
        if expiry:
            try:
                exp = datetime.datetime.fromisoformat(expiry.replace("Z", "+00:00"))
                if datetime.datetime.now(datetime.timezone.utc) >= exp:
                    refresh = data.get("refresh_token", "")
                    if isinstance(data.get("token"), dict): refresh = data["token"].get("refresh_token", refresh)
                    if refresh:
                        body = urllib.parse.urlencode({"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "refresh_token": refresh, "grant_type": "refresh_token"}).encode()
                        req = urllib.request.Request(TOKEN_URI, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"})
                        r = urllib.request.urlopen(req, timeout=10, context=ssl._create_unverified_context())
                        tok_data = json.loads(r.read())
                        access = tok_data.get("access_token", access)
            except: pass
        return access
    except: return None

@app.get("/api/vps")
async def get_vps():
    cpu = _run(["bash", "-c", "top -bn1 2>/dev/null | head -5 | grep 'Cpu(s)' | awk '{print $2}'"])
    mem_raw = _run(["bash", "-c", "free -m | grep Mem:"])
    disk_raw = _run(["bash", "-c", "df -h / | tail -1"])
    uptime = _run(["uptime", "-p"])
    load = _run(["bash", "-c", "cat /proc/loadavg | awk '{print $1\" \"$2\" \"$3}'"])
    mem_parts = mem_raw.split()
    mem = {"total": mem_parts[1] if len(mem_parts) > 1 else "?", "used": mem_parts[2] if len(mem_parts) > 2 else "?"}
    disk_parts = disk_raw.split()
    disk = {"total": disk_parts[1] if len(disk_parts) > 1 else "?", "used": disk_parts[2] if len(disk_parts) > 2 else "?", "pct": disk_parts[4] if len(disk_parts) > 4 else "?"}
    return {"cpu": cpu, "mem": mem, "disk": disk, "uptime": uptime, "load": load}

@app.get("/api/docker")
async def get_docker():
    raw = _run(["docker", "ps", "--format", "{{json .}}"], timeout=15)
    containers = []
    for line in raw.split("\n"):
        line = line.strip()
        if not line: continue
        try: containers.append(json.loads(line))
        except: pass
    stats_raw = _run(["docker", "stats", "--no-stream", "--format", "{{json .}}"], timeout=15)
    stats_map = {}
    for line in stats_raw.split("\n"):
        line = line.strip()
        if not line: continue
        try:
            s = json.loads(line)
            stats_map[s.get("Name")] = {"cpu": s.get("CPUPerc", "?"), "mem": s.get("MemPerc", "?")}
        except: pass
    for c in containers:
        s = stats_map.get(c.get("Name") or c.get("name", ""))
        if s: c["stats"] = s
    return {"containers": [{"name": c.get("Names") or c.get("name", "?"), "image": c.get("Image") or c.get("image", "?"), "status": c.get("Status") or c.get("status", "?"), "ports": c.get("Ports") or c.get("ports", ""), "state": c.get("State") or c.get("state", "?"), "stats": c.get("stats", {})} for c in containers]}

SITES = [
    {"name": "HCI Dashboard", "url": "https://144.91.81.173:8443", "icon": "🖥️", "check": "https://localhost:8443"},
    {"name": "Catálogo", "url": "https://144.91.81.173:8444", "icon": "📂", "check": "https://localhost:8444"},
    {"name": "Dashboard Akira", "url": "https://144.91.81.173:8586", "icon": "📊", "check": "https://localhost:8586"},
    {"name": "Tarifario", "url": "https://144.91.81.173:8443/tarifario/", "icon": "💰", "check": "https://localhost:8443/tarifario/"},
    {"name": "SilverBullet", "url": "https://144.91.81.173:3002", "icon": "📝", "check": "https://localhost:3002"},
    {"name": "Analizador", "url": "https://juanmartinezgarcia.com/analizador", "icon": "🎨", "check": "https://juanmartinezgarcia.com/analizador"},
    {"name": "Akira Mind", "url": "https://144.91.81.173:8535", "icon": "🧠", "check": "https://localhost:8535"},
]

@app.get("/api/sites")
async def get_sites():
    results = []
    for site in SITES:
        status = "unknown"
        check_url = site.get("check", site["url"])
        try:
            ctx = ssl._create_unverified_context()
            r = urllib.request.urlopen(check_url, timeout=5, context=ctx)
            status = "up" if r.status < 400 else "degraded"
        except urllib.error.HTTPError as e:
            # HTTP errors (401, 403, etc.) mean the server IS responding
            status = "up"
        except Exception:
            status = "down"
        results.append({"name": site["name"], "url": site["url"], "icon": site["icon"], "status": status})
    return {"sites": results}

@app.get("/api/notas")
async def get_notas():
    if not os.path.isdir(NOTAS_DIR): return {"notas": []}
    try:
        notas = []
        for f in sorted(os.listdir(NOTAS_DIR), reverse=True)[:12]:
            fpath = os.path.join(NOTAS_DIR, f)
            if os.path.isfile(fpath) and f.endswith(".md"):
                mod = datetime.datetime.fromtimestamp(os.path.getmtime(fpath)).isoformat()
                notas.append({"title": f.replace(".md", ""), "modified": mod})
        return {"notas": notas}
    except: return {"notas": []}

@app.get("/api/github")
async def get_github():
    try:
        req = urllib.request.Request("https://api.github.com/users/juanaustral/repos?sort=updated&per_page=6&type=all",
                                     headers={"User-Agent": "Dashboard-Akira", "Accept": "application/vnd.github.v3+json"})
        ctx = ssl._create_unverified_context()
        r = urllib.request.urlopen(req, timeout=10, context=ctx)
        repos = json.loads(r.read())
        return {"repos": [{"name": r["name"], "description": r.get("description",""), "stars": r.get("stargazers_count",0), "forks": r.get("forks_count",0), "language": r.get("language",""), "updated": r.get("updated_at",""), "url": r["html_url"]} for r in repos]}
    except Exception as e: return {"repos": [], "error": str(e)[:80]}

@app.get("/api/tasks")
async def get_tasks():
    token = _get_google_token()
    if not token: return {"tasks": [], "error": "No Google token"}
    try:
        ctx = ssl._create_unverified_context()
        req = urllib.request.Request("https://tasks.googleapis.com/tasks/v1/lists/@default/tasks?maxResults=20&showCompleted=false",
                                     headers={"Authorization": f"Bearer {token}"})
        r = urllib.request.urlopen(req, timeout=10, context=ctx)
        data = json.loads(r.read())
        return {"tasks": [{"title": t.get("title",""), "notes": t.get("notes","") or "", "due": t.get("due",""), "status": t.get("status","")} for t in data.get("items",[])]}
    except Exception as e: return {"tasks": [], "error": str(e)[:80]}

@app.get("/api/calendar")
async def get_calendar():
    token = _get_google_token()
    if not token: return {"events": [], "error": "No Google token"}
    try:
        now = datetime.datetime.utcnow().isoformat() + "Z"
        ctx = ssl._create_unverified_context()
        req = urllib.request.Request(
            f"https://www.googleapis.com/calendar/v3/calendars/primary/events?timeMin={now}&maxResults=20&orderBy=startTime&singleEvents=true",
            headers={"Authorization": f"Bearer {token}"})
        r = urllib.request.urlopen(req, timeout=10, context=ctx)
        data = json.loads(r.read())
        events = []
        for e in data.get("items", []):
            start = e.get("start", {}).get("dateTime") or e.get("start", {}).get("date", "")
            events.append({"summary": e.get("summary",""), "start": start, "location": e.get("location","") or ""})
        return {"events": events}
    except Exception as e: return {"events": [], "error": str(e)[:100]}

@app.get("/api/deepseek")
async def get_deepseek():
    if not DEEPSEEK_KEY: return {"available": False}
    try:
        ctx = ssl._create_unverified_context()
        req = urllib.request.Request("https://api.deepseek.com/user/balance",
                                     headers={"Authorization": f"Bearer {DEEPSEEK_KEY}", "Accept": "application/json"})
        r = urllib.request.urlopen(req, timeout=10, context=ctx)
        data = json.loads(r.read())
        if not data.get("is_available"): return {"available": False}
        for b in data.get("balance_infos", []):
            if b.get("currency") == "USD": return {"available": True, "balance": b["total_balance"]}
        return {"available": True, "balance": "?"}
    except: return {"available": False, "error": "API error"}

@app.post("/api/tasks/complete")
async def complete_task(data: dict):
    """Mark a task as completed."""
    token = _get_google_token()
    if not token: raise HTTPException(401, "No Google token")
    task_id = data.get("id", "")
    if not task_id: raise HTTPException(400, "Missing task id")
    try:
        body = json.dumps({"status": "completed"}).encode()
        req = urllib.request.Request(
            f"https://tasks.googleapis.com/tasks/v1/lists/@default/tasks/{task_id}",
            data=body, method="PATCH",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
        ctx = ssl._create_unverified_context()
        urllib.request.urlopen(req, timeout=10, context=ctx)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(500, str(e)[:100])

@app.post("/api/tasks/create")
async def create_task(data: dict):
    """Create a new task."""
    token = _get_google_token()
    if not token: raise HTTPException(401, "No Google token")
    title = data.get("title", "").strip()
    if not title: raise HTTPException(400, "Missing title")
    notes = data.get("notes", "")
    due = data.get("due", "")
    try:
        task = {"title": title, "notes": notes}
        if due: task["due"] = due + "T00:00:00.000Z"
        body = json.dumps(task).encode()
        req = urllib.request.Request(
            "https://tasks.googleapis.com/tasks/v1/lists/@default/tasks",
            data=body, method="POST",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
        ctx = ssl._create_unverified_context()
        r = urllib.request.urlopen(req, timeout=10, context=ctx)
        return json.loads(r.read())
    except Exception as e:
        raise HTTPException(500, str(e)[:100])

# ── Chat endpoint ───────────────────────────────────────────────────────
@app.post("/api/chat")
async def chat_endpoint(data: dict):
    """Send message to DeepSeek and return response."""
    if not DEEPSEEK_KEY:
        return {"response": "DeepSeek API key no configurada."}
    messages = data.get("messages", [])
    if not messages:
        return {"response": "Envia al menos un mensaje."}
    try:
        body = json.dumps({
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000
        }).encode()
        req = urllib.request.Request("https://api.deepseek.com/v1/chat/completions",
            data=body, headers={"Authorization": f"Bearer {DEEPSEEK_KEY}", "Content-Type": "application/json"})
        ctx = ssl._create_unverified_context()
        r = urllib.request.urlopen(req, timeout=60, context=ctx)
        resp = json.loads(r.read())
        return {"response": resp["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"response": f"Error: {str(e)[:200]}"}

# ── Notas CRUD ──────────────────────────────────────────────────────────
@app.get("/api/notas/tree")
async def get_notas_tree():
    """Get hierarchical tree of all notes."""
    if not os.path.isdir(NOTAS_DIR): return {"tree": []}
    def scan(path, prefix=""):
        items = []
        try:
            for name in sorted(os.listdir(path)):
                full = os.path.join(path, name)
                rel = os.path.join(prefix, name) if prefix else name
                if name.startswith(".") or name == "SETTINGS.md": continue
                if os.path.isdir(full):
                    children = scan(full, rel)
                    if children:
                        items.append({"name": name, "path": rel, "type": "folder", "children": children})
                elif name.endswith(".md"):
                    mod = datetime.datetime.fromtimestamp(os.path.getmtime(full)).isoformat()
                    size = os.path.getsize(full)
                    items.append({"name": name.replace(".md",""), "path": rel, "type": "file", "modified": mod, "size": size})
        except: pass
        return items
    return {"tree": scan(NOTAS_DIR)}

@app.get("/api/notas/read")
async def read_nota(path: str = ""):
    """Read a specific note file."""
    if not path or ".." in path:
        raise HTTPException(400, "Ruta invalida")
    fpath = os.path.join(NOTAS_DIR, path)
    if not os.path.isfile(fpath):
        raise HTTPException(404, "Nota no encontrada")
    try:
        content = Path(fpath).read_text()
        return {"path": path, "content": content}
    except:
        raise HTTPException(500, "Error al leer la nota")

@app.post("/api/notas/write")
async def write_nota(data: dict):
    """Create or update a note file."""
    path = data.get("path", "")
    content = data.get("content", "")
    if not path or ".." in path:
        raise HTTPException(400, "Ruta invalida")
    fpath = os.path.join(NOTAS_DIR, path)
    os.makedirs(os.path.dirname(fpath), exist_ok=True)
    Path(fpath).write_text(content)
    return {"ok": True, "path": path}

@app.delete("/api/notas/delete")
async def delete_nota(data: dict):
    """Delete a note file."""
    path = data.get("path", "")
    if not path or ".." in path:
        raise HTTPException(400, "Ruta invalida")
    fpath = os.path.join(NOTAS_DIR, path)
    if os.path.isfile(fpath):
        os.remove(fpath)
        return {"ok": True}
    raise HTTPException(404, "Nota no encontrada")

@app.get("/api/all")
async def get_all():
    vps, docker, sites, notas, github, tasks, cal, ds = await asyncio.gather(
        get_vps(), get_docker(), get_sites(), get_notas(),
        get_github(), get_tasks(), get_calendar(), get_deepseek(), return_exceptions=True)
    def safe(r): return r if not isinstance(r, Exception) else {"error": str(r)}
    return {"vps": safe(vps), "docker": safe(docker), "sites": safe(sites), "notas": safe(notas),
            "github": safe(github), "tasks": safe(tasks), "calendar": safe(cal), "deepseek": safe(ds)}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    while True:
        try:
            data = await get_all()
            await ws.send_json(data)
            await asyncio.sleep(10)
        except: break

static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8585))
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
