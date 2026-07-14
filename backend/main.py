#!/usr/bin/env python3
"""Dashboard — Backend FastAPI (puerto 8585)"""
import asyncio, json, os, subprocess, sys, urllib.request, urllib.parse, urllib.error
import ssl, re, datetime, time
from pathlib import Path
from fastapi import FastAPI, WebSocket, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# ── SQLAlchemy + SQLite ──────────────────────────────────────────────────
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime as dt

DB_PATH = Path(__file__).parent.parent / "data" / "dashboard.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()

# ── Modelos ──────────────────────────────────────────────────────────────

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    category = Column(String, default="")
    due_day = Column(Integer, default=1)
    billing_cycle = Column(String, default="monthly")  # monthly / yearly
    notes = Column(Text, default="")
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=dt.utcnow)
    updated_at = Column(DateTime, default=dt.utcnow, onupdate=dt.utcnow)

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=True)
    description = Column(String, default="")
    amount = Column(Float, nullable=False)
    category = Column(String, default="")
    date = Column(String, default="")  # YYYY-MM-DD
    payment_method = Column(String, default="")
    is_recurring = Column(Boolean, default=False)
    created_at = Column(DateTime, default=dt.utcnow)
    service = relationship("Service")

class CreditCard(Base):
    __tablename__ = "credit_cards"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    closing_day = Column(Integer, default=1)
    due_day = Column(Integer, default=15)
    limit_amount = Column(Float, default=0.0)
    created_at = Column(DateTime, default=dt.utcnow)

class CreditCardStatement(Base):
    __tablename__ = "credit_card_statements"
    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("credit_cards.id"), nullable=False)
    period = Column(String, nullable=False)  # YYYY-MM
    total_amount = Column(Float, default=0.0)
    is_paid = Column(Boolean, default=False)
    due_date = Column(String, default="")
    closing_date = Column(String, default="")
    notes = Column(Text, default="")
    created_at = Column(DateTime, default=dt.utcnow)
    card = relationship("CreditCard")

class ListItem(Base):
    __tablename__ = "list_items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    type = Column(String, default="other")     # movie/series/music/place/food/other
    status = Column(String, default="planned")  # planned/watching/watched/abandoned
    rating = Column(Integer, nullable=True)     # 1-5
    notes = Column(Text, default="")
    external_id = Column(String, default="")    # TMDB ID
    image_url = Column(String, default="")
    category = Column(String, default="")
    created_at = Column(DateTime, default=dt.utcnow)
    updated_at = Column(DateTime, default=dt.utcnow, onupdate=dt.utcnow)

class ListCategory(Base):
    __tablename__ = "list_categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, default="")
    color = Column(String, default="")
    icon = Column(String, default="")
    created_at = Column(DateTime, default=dt.utcnow)

Base.metadata.create_all(bind=engine)

# ── Helper ───────────────────────────────────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def _get_tmdb_key():
    """Read TMDB_API_KEY from .hermes/.env, os.environ, or return None."""
    key = os.environ.get("TMDB_API_KEY")
    if key: return key
    try:
        with open("/root/.hermes/.env") as f:
            for line in f:
                line = line.strip()
                if line.startswith("TMDB_API_KEY="):
                    return line.split("=", 1)[1].strip().strip("\"'")
    except: pass
    try:
        from hermes_cli.config import get_env_value
        val = get_env_value("TMDB_API_KEY")
        if val: return val
    except: pass
    return None

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
                    break
    except: pass


# ── Cache en memoria (60s TTL) ──
# ── Cache en memoria (60s TTL) ────────────────────────────────────────────
_cache: dict[str, tuple[float, object]] = {}  # key -> (expiry_timestamp, value)
_CACHE_TTL = 60  # seconds

def _cache_get(key: str):
    """Return cached value if fresh, else None."""
    entry = _cache.get(key)
    if entry is None:
        return None
    expiry, value = entry
    if time.time() < expiry:
        return value
    del _cache[key]
    return None

def _cache_set(key: str, value: object):
    """Store value in cache with TTL."""
    _cache[key] = (time.time() + _CACHE_TTL, value)

# ── Timeout wrapper ──────────────────────────────────────────────────────
async def _call_with_timeout(coro, timeout=2.0, fallback=None):
    """Run an async call with timeout. Returns fallback on timeout/error."""
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        return fallback if fallback is not None else {"error": "timeout", "available": False}
    except Exception as e:
        return fallback if fallback is not None else {"error": str(e)[:80], "available": False}

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
    cached = _cache_get("tasks")
    if cached is not None:
        return cached
    token = _get_google_token()
    if not token:
        result = {"tasks": [], "error": "No Google token"}
        _cache_set("tasks", result)
        return result
    try:
        ctx = ssl._create_unverified_context()
        req = urllib.request.Request("https://tasks.googleapis.com/tasks/v1/lists/@default/tasks?maxResults=20&showCompleted=false",
                                     headers={"Authorization": f"Bearer {token}"})
        r = await asyncio.to_thread(lambda: urllib.request.urlopen(req, timeout=2, context=ctx))
        data = json.loads(r.read())
        result = {"tasks": [{"title": t.get("title",""), "notes": t.get("notes","") or "", "due": t.get("due",""), "status": t.get("status","")} for t in data.get("items",[])]}
        _cache_set("tasks", result)
        return result
    except asyncio.TimeoutError:
        return {"tasks": [], "error": "timeout"}
    except Exception as e:
        return {"tasks": [], "error": str(e)[:80]}

@app.get("/api/calendar")
async def get_calendar():
    cached = _cache_get("calendar")
    if cached is not None:
        return cached
    token = _get_google_token()
    if not token:
        result = {"events": [], "error": "No Google token"}
        _cache_set("calendar", result)
        return result
    try:
        now = datetime.datetime.utcnow().isoformat() + "Z"
        ctx = ssl._create_unverified_context()
        req = urllib.request.Request(
            f"https://www.googleapis.com/calendar/v3/calendars/primary/events?timeMin={now}&maxResults=20&orderBy=startTime&singleEvents=true",
            headers={"Authorization": f"Bearer {token}"})
        r = await asyncio.to_thread(lambda: urllib.request.urlopen(req, timeout=2, context=ctx))
        data = json.loads(r.read())
        events = []
        for e in data.get("items", []):
            start = e.get("start", {}).get("dateTime") or e.get("start", {}).get("date", "")
            events.append({"summary": e.get("summary",""), "start": start, "location": e.get("location","") or ""})
        result = {"events": events}
        _cache_set("calendar", result)
        return result
    except asyncio.TimeoutError:
        return {"events": [], "error": "timeout"}
    except Exception as e:
        return {"events": [], "error": str(e)[:100]}

@app.get("/api/deepseek")
async def get_deepseek():
    if not DEEPSEEK_KEY: return {"available": False}
    cached = _cache_get("deepseek")
    if cached is not None:
        return cached
    try:
        ctx = ssl._create_unverified_context()
        req = urllib.request.Request("https://api.deepseek.com/user/balance",
                                     headers={"Authorization": f"Bearer {DEEPSEEK_KEY}", "Accept": "application/json"})
        r = await asyncio.to_thread(lambda: urllib.request.urlopen(req, timeout=2, context=ctx))
        data = json.loads(r.read())
        if not data.get("is_available"):
            result = {"available": False}
        else:
            result = None
            for b in data.get("balance_infos", []):
                if b.get("currency") == "USD":
                    result = {"available": True, "balance": b["total_balance"]}
                    break
            if result is None:
                result = {"available": True, "balance": "?"}
        _cache_set("deepseek", result)
        return result
    except asyncio.TimeoutError:
        result = {"available": False, "error": "timeout"}
        return result
    except Exception as e:
        result = {"available": False, "error": str(e)[:80]}
        return result

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
    """Gather all dashboard data with 2s timeout per endpoint and cache."""
    timeout = 2.0
    vps, docker, sites, notas, github, tasks, cal, ds = await asyncio.gather(
        _call_with_timeout(get_vps(), timeout=timeout),
        _call_with_timeout(get_docker(), timeout=timeout),
        _call_with_timeout(get_sites(), timeout=timeout),
        _call_with_timeout(get_notas(), timeout=timeout),
        _call_with_timeout(get_github(), timeout=timeout),
        _call_with_timeout(get_tasks(), timeout=timeout),
        _call_with_timeout(get_calendar(), timeout=timeout),
        _call_with_timeout(get_deepseek(), timeout=timeout),
        return_exceptions=True)
    def safe(r): return r if not isinstance(r, Exception) else {"error": str(r)[:80]}
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

# ═══════════════════════════════════════════════════════════════════════════
# ── FINANZAS: Services ───────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════

@app.get("/api/finanzas/services")
async def list_services():
    db = SessionLocal()
    try:
        items = db.query(Service).order_by(Service.name).all()
        return {"services": [{"id": s.id, "name": s.name, "amount": s.amount,
            "currency": s.currency, "category": s.category, "due_day": s.due_day,
            "billing_cycle": s.billing_cycle, "notes": s.notes, "active": s.active,
            "created_at": s.created_at.isoformat() if s.created_at else None,
            "updated_at": s.updated_at.isoformat() if s.updated_at else None} for s in items]}
    finally:
        db.close()

@app.post("/api/finanzas/services")
async def create_service(data: dict):
    db = SessionLocal()
    try:
        s = Service(name=data["name"], amount=float(data.get("amount", 0)),
            currency=data.get("currency", "USD"), category=data.get("category", ""),
            due_day=int(data.get("due_day", 1)),
            billing_cycle=data.get("billing_cycle", "monthly"),
            notes=data.get("notes", ""), active=data.get("active", True))
        db.add(s); db.commit(); db.refresh(s)
        return {"id": s.id}
    except Exception as e:
        db.rollback(); raise HTTPException(400, str(e))
    finally:
        db.close()

@app.get("/api/finanzas/services/{sid}")
async def read_service(sid: int):
    db = SessionLocal()
    try:
        s = db.query(Service).get(sid)
        if not s: raise HTTPException(404, "Service not found")
        return {"id": s.id, "name": s.name, "amount": s.amount, "currency": s.currency,
            "category": s.category, "due_day": s.due_day, "billing_cycle": s.billing_cycle,
            "notes": s.notes, "active": s.active,
            "created_at": s.created_at.isoformat() if s.created_at else None,
            "updated_at": s.updated_at.isoformat() if s.updated_at else None}
    finally:
        db.close()

@app.put("/api/finanzas/services/{sid}")
async def update_service(sid: int, data: dict):
    db = SessionLocal()
    try:
        s = db.query(Service).get(sid)
        if not s: raise HTTPException(404, "Service not found")
        for k in ("name","currency","category","notes","billing_cycle"):
            if k in data: setattr(s, k, data[k])
        if "amount" in data: s.amount = float(data["amount"])
        if "due_day" in data: s.due_day = int(data["due_day"])
        if "active" in data: s.active = bool(data["active"])
        s.updated_at = dt.utcnow()
        db.commit()
        return {"ok": True}
    except Exception as e:
        db.rollback(); raise HTTPException(400, str(e))
    finally:
        db.close()

@app.delete("/api/finanzas/services/{sid}")
async def delete_service(sid: int):
    db = SessionLocal()
    try:
        s = db.query(Service).get(sid)
        if not s: raise HTTPException(404, "Service not found")
        db.delete(s); db.commit()
        return {"ok": True}
    finally:
        db.close()

# ── FINANZAS: Expenses ────────────────────────────────────────────────────

@app.get("/api/finanzas/expenses")
async def list_expenses():
    db = SessionLocal()
    try:
        items = db.query(Expense).order_by(Expense.date.desc().nullslast(), Expense.created_at.desc()).all()
        return {"expenses": [{"id": e.id, "service_id": e.service_id, "description": e.description,
            "amount": e.amount, "category": e.category, "date": e.date,
            "payment_method": e.payment_method, "is_recurring": e.is_recurring,
            "created_at": e.created_at.isoformat() if e.created_at else None} for e in items]}
    finally:
        db.close()

@app.post("/api/finanzas/expenses")
async def create_expense(data: dict):
    db = SessionLocal()
    try:
        e = Expense(service_id=data.get("service_id"), description=data.get("description",""),
            amount=float(data.get("amount",0)), category=data.get("category",""),
            date=data.get("date",""), payment_method=data.get("payment_method",""),
            is_recurring=data.get("is_recurring",False))
        db.add(e); db.commit(); db.refresh(e)
        return {"id": e.id}
    except Exception as ex:
        db.rollback(); raise HTTPException(400, str(ex))
    finally:
        db.close()

@app.get("/api/finanzas/expenses/{eid}")
async def read_expense(eid: int):
    db = SessionLocal()
    try:
        e = db.query(Expense).get(eid)
        if not e: raise HTTPException(404, "Expense not found")
        return {"id": e.id, "service_id": e.service_id, "description": e.description,
            "amount": e.amount, "category": e.category, "date": e.date,
            "payment_method": e.payment_method, "is_recurring": e.is_recurring,
            "created_at": e.created_at.isoformat() if e.created_at else None}
    finally:
        db.close()

@app.put("/api/finanzas/expenses/{eid}")
async def update_expense(eid: int, data: dict):
    db = SessionLocal()
    try:
        e = db.query(Expense).get(eid)
        if not e: raise HTTPException(404, "Expense not found")
        for k in ("service_id","description","category","date","payment_method"):
            if k in data: setattr(e, k, data[k])
        if "amount" in data: e.amount = float(data["amount"])
        if "is_recurring" in data: e.is_recurring = bool(data["is_recurring"])
        db.commit()
        return {"ok": True}
    except Exception as ex:
        db.rollback(); raise HTTPException(400, str(ex))
    finally:
        db.close()

@app.delete("/api/finanzas/expenses/{eid}")
async def delete_expense(eid: int):
    db = SessionLocal()
    try:
        e = db.query(Expense).get(eid)
        if not e: raise HTTPException(404, "Expense not found")
        db.delete(e); db.commit()
        return {"ok": True}
    finally:
        db.close()

# ── FINANZAS: Credit Cards ────────────────────────────────────────────────

@app.get("/api/finanzas/credit-cards")
async def list_credit_cards():
    db = SessionLocal()
    try:
        items = db.query(CreditCard).order_by(CreditCard.name).all()
        return {"credit_cards": [{"id": c.id, "name": c.name, "closing_day": c.closing_day,
            "due_day": c.due_day, "limit_amount": c.limit_amount,
            "created_at": c.created_at.isoformat() if c.created_at else None} for c in items]}
    finally:
        db.close()

@app.post("/api/finanzas/credit-cards")
async def create_credit_card(data: dict):
    db = SessionLocal()
    try:
        c = CreditCard(name=data["name"], closing_day=int(data.get("closing_day",1)),
            due_day=int(data.get("due_day",15)), limit_amount=float(data.get("limit_amount",0)))
        db.add(c); db.commit(); db.refresh(c)
        return {"id": c.id}
    except Exception as ex:
        db.rollback(); raise HTTPException(400, str(ex))
    finally:
        db.close()

@app.get("/api/finanzas/credit-cards/{cid}")
async def read_credit_card(cid: int):
    db = SessionLocal()
    try:
        c = db.query(CreditCard).get(cid)
        if not c: raise HTTPException(404, "Credit card not found")
        return {"id": c.id, "name": c.name, "closing_day": c.closing_day,
            "due_day": c.due_day, "limit_amount": c.limit_amount,
            "created_at": c.created_at.isoformat() if c.created_at else None}
    finally:
        db.close()

@app.put("/api/finanzas/credit-cards/{cid}")
async def update_credit_card(cid: int, data: dict):
    db = SessionLocal()
    try:
        c = db.query(CreditCard).get(cid)
        if not c: raise HTTPException(404, "Credit card not found")
        for k in ("name",):
            if k in data: setattr(c, k, data[k])
        if "closing_day" in data: c.closing_day = int(data["closing_day"])
        if "due_day" in data: c.due_day = int(data["due_day"])
        if "limit_amount" in data: c.limit_amount = float(data["limit_amount"])
        db.commit()
        return {"ok": True}
    except Exception as ex:
        db.rollback(); raise HTTPException(400, str(ex))
    finally:
        db.close()

@app.delete("/api/finanzas/credit-cards/{cid}")
async def delete_credit_card(cid: int):
    db = SessionLocal()
    try:
        c = db.query(CreditCard).get(cid)
        if not c: raise HTTPException(404, "Credit card not found")
        db.delete(c); db.commit()
        return {"ok": True}
    finally:
        db.close()

# ── FINANZAS: Credit Card Statements ──────────────────────────────────────

@app.get("/api/finanzas/credit-card-statements")
async def list_credit_card_statements():
    db = SessionLocal()
    try:
        items = db.query(CreditCardStatement).order_by(CreditCardStatement.period.desc()).all()
        return {"statements": [{"id": st.id, "card_id": st.card_id, "period": st.period,
            "total_amount": st.total_amount, "is_paid": st.is_paid, "due_date": st.due_date,
            "closing_date": st.closing_date, "notes": st.notes,
            "created_at": st.created_at.isoformat() if st.created_at else None} for st in items]}
    finally:
        db.close()

@app.post("/api/finanzas/credit-card-statements")
async def create_credit_card_statement(data: dict):
    db = SessionLocal()
    try:
        st = CreditCardStatement(card_id=int(data["card_id"]), period=data["period"],
            total_amount=float(data.get("total_amount",0)),
            is_paid=data.get("is_paid",False), due_date=data.get("due_date",""),
            closing_date=data.get("closing_date",""), notes=data.get("notes",""))
        db.add(st); db.commit(); db.refresh(st)
        return {"id": st.id}
    except Exception as ex:
        db.rollback(); raise HTTPException(400, str(ex))
    finally:
        db.close()

@app.get("/api/finanzas/credit-card-statements/{sid}")
async def read_credit_card_statement(sid: int):
    db = SessionLocal()
    try:
        st = db.query(CreditCardStatement).get(sid)
        if not st: raise HTTPException(404, "Statement not found")
        return {"id": st.id, "card_id": st.card_id, "period": st.period,
            "total_amount": st.total_amount, "is_paid": st.is_paid, "due_date": st.due_date,
            "closing_date": st.closing_date, "notes": st.notes,
            "created_at": st.created_at.isoformat() if st.created_at else None}
    finally:
        db.close()

@app.put("/api/finanzas/credit-card-statements/{sid}")
async def update_credit_card_statement(sid: int, data: dict):
    db = SessionLocal()
    try:
        st = db.query(CreditCardStatement).get(sid)
        if not st: raise HTTPException(404, "Statement not found")
        for k in ("period","due_date","closing_date","notes"):
            if k in data: setattr(st, k, data[k])
        if "card_id" in data: st.card_id = int(data["card_id"])
        if "total_amount" in data: st.total_amount = float(data["total_amount"])
        if "is_paid" in data: st.is_paid = bool(data["is_paid"])
        db.commit()
        return {"ok": True}
    except Exception as ex:
        db.rollback(); raise HTTPException(400, str(ex))
    finally:
        db.close()

@app.delete("/api/finanzas/credit-card-statements/{sid}")
async def delete_credit_card_statement(sid: int):
    db = SessionLocal()
    try:
        st = db.query(CreditCardStatement).get(sid)
        if not st: raise HTTPException(404, "Statement not found")
        db.delete(st); db.commit()
        return {"ok": True}
    finally:
        db.close()

# ── FINANZAS: Summary ─────────────────────────────────────────────────────

@app.get("/api/finanzas/summary")
async def finanzas_summary():
    db = SessionLocal()
    try:
        today = dt.utcnow()
        today_day = today.day
        today_str = today.strftime("%Y-%m-%d")

        # All active services
        services = db.query(Service).filter(Service.active == True).all()
        total_monthly = 0.0
        total_yearly = 0.0
        category_breakdown = {}

        for s in services:
            amt = s.amount
            if s.billing_cycle == "yearly":
                total_yearly += amt
                m_equiv = amt / 12.0
            else:
                m_equiv = amt
            total_monthly += m_equiv

            cat = s.category or "uncategorized"
            category_breakdown.setdefault(cat, {"monthly": 0.0, "count": 0})
            category_breakdown[cat]["monthly"] += m_equiv
            category_breakdown[cat]["count"] += 1

        # Upcoming payments (services due within 30 days)
        upcoming = []
        from datetime import timedelta
        for s in services:
            dd = s.due_day
            # Figure out next due date
            try:
                if dd >= today_day:
                    next_due = today.replace(day=dd)
                else:
                    next_m = today.month + 1
                    next_y = today.year
                    if next_m > 12:
                        next_m = 1; next_y += 1
                    next_due = today.replace(year=next_y, month=next_m, day=min(dd, 28))
                if next_due <= today + timedelta(days=30):
                    upcoming.append({
                        "name": s.name, "amount": s.amount, "currency": s.currency,
                        "due_date": next_due.strftime("%Y-%m-%d"),
                        "category": s.category, "billing_cycle": s.billing_cycle
                    })
            except:
                pass

        # Add recurring expenses to upcoming
        expenses = db.query(Expense).filter(Expense.is_recurring == True).all()
        for e in expenses:
            upcoming.append({
                "name": e.description or "Expense",
                "amount": e.amount, "currency": "USD",
                "due_date": e.date or today_str,
                "category": e.category, "billing_cycle": "monthly"
            })

        upcoming.sort(key=lambda x: x["due_date"])

        return {
            "total_monthly": round(total_monthly, 2),
            "total_yearly": round(total_yearly + total_monthly * 12, 2),
            "upcoming_payments": upcoming[:30],
            "category_breakdown": {k: {**v, "monthly": round(v["monthly"], 2)} for k, v in category_breakdown.items()}
        }
    finally:
        db.close()

# ═══════════════════════════════════════════════════════════════════════════
# ── LISTAS ────────────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════

@app.get("/api/listas/items")
async def list_list_items():
    db = SessionLocal()
    try:
        items = db.query(ListItem).order_by(ListItem.created_at.desc()).all()
        return {"items": [{"id": i.id, "title": i.title, "type": i.type,
            "status": i.status, "rating": i.rating, "notes": i.notes,
            "external_id": i.external_id, "image_url": i.image_url, "category": i.category,
            "created_at": i.created_at.isoformat() if i.created_at else None,
            "updated_at": i.updated_at.isoformat() if i.updated_at else None} for i in items]}
    finally:
        db.close()

@app.post("/api/listas/items")
async def create_list_item(data: dict):
    db = SessionLocal()
    try:
        rating = data.get("rating")
        if rating is not None: rating = int(rating)
        i = ListItem(title=data["title"], type=data.get("type","other"),
            status=data.get("status","planned"), rating=rating,
            notes=data.get("notes",""), external_id=data.get("external_id",""),
            image_url=data.get("image_url",""), category=data.get("category",""))
        db.add(i); db.commit(); db.refresh(i)
        return {"id": i.id}
    except Exception as ex:
        db.rollback(); raise HTTPException(400, str(ex))
    finally:
        db.close()

@app.get("/api/listas/items/{iid}")
async def read_list_item(iid: int):
    db = SessionLocal()
    try:
        i = db.query(ListItem).get(iid)
        if not i: raise HTTPException(404, "Item not found")
        return {"id": i.id, "title": i.title, "type": i.type, "status": i.status,
            "rating": i.rating, "notes": i.notes, "external_id": i.external_id,
            "image_url": i.image_url, "category": i.category,
            "created_at": i.created_at.isoformat() if i.created_at else None,
            "updated_at": i.updated_at.isoformat() if i.updated_at else None}
    finally:
        db.close()

@app.put("/api/listas/items/{iid}")
async def update_list_item(iid: int, data: dict):
    db = SessionLocal()
    try:
        i = db.query(ListItem).get(iid)
        if not i: raise HTTPException(404, "Item not found")
        for k in ("title","type","status","notes","external_id","image_url","category"):
            if k in data: setattr(i, k, data[k])
        if "rating" in data:
            v = data["rating"]
            i.rating = int(v) if v is not None else None
        i.updated_at = dt.utcnow()
        db.commit()
        return {"ok": True}
    except Exception as ex:
        db.rollback(); raise HTTPException(400, str(ex))
    finally:
        db.close()

@app.delete("/api/listas/items/{iid}")
async def delete_list_item(iid: int):
    db = SessionLocal()
    try:
        i = db.query(ListItem).get(iid)
        if not i: raise HTTPException(404, "Item not found")
        db.delete(i); db.commit()
        return {"ok": True}
    finally:
        db.close()

# ── LISTAS: Categories ────────────────────────────────────────────────────

@app.get("/api/listas/categories")
async def list_list_categories():
    db = SessionLocal()
    try:
        items = db.query(ListCategory).order_by(ListCategory.name).all()
        return {"categories": [{"id": c.id, "name": c.name, "type": c.type,
            "color": c.color, "icon": c.icon,
            "created_at": c.created_at.isoformat() if c.created_at else None} for c in items]}
    finally:
        db.close()

@app.post("/api/listas/categories")
async def create_list_category(data: dict):
    db = SessionLocal()
    try:
        c = ListCategory(name=data["name"], type=data.get("type",""),
            color=data.get("color",""), icon=data.get("icon",""))
        db.add(c); db.commit(); db.refresh(c)
        return {"id": c.id}
    except Exception as ex:
        db.rollback(); raise HTTPException(400, str(ex))
    finally:
        db.close()

@app.get("/api/listas/categories/{cid}")
async def read_list_category(cid: int):
    db = SessionLocal()
    try:
        c = db.query(ListCategory).get(cid)
        if not c: raise HTTPException(404, "Category not found")
        return {"id": c.id, "name": c.name, "type": c.type, "color": c.color, "icon": c.icon,
            "created_at": c.created_at.isoformat() if c.created_at else None}
    finally:
        db.close()

@app.put("/api/listas/categories/{cid}")
async def update_list_category(cid: int, data: dict):
    db = SessionLocal()
    try:
        c = db.query(ListCategory).get(cid)
        if not c: raise HTTPException(404, "Category not found")
        for k in ("name","type","color","icon"):
            if k in data: setattr(c, k, data[k])
        db.commit()
        return {"ok": True}
    except Exception as ex:
        db.rollback(); raise HTTPException(400, str(ex))
    finally:
        db.close()

@app.delete("/api/listas/categories/{cid}")
async def delete_list_category(cid: int):
    db = SessionLocal()
    try:
        c = db.query(ListCategory).get(cid)
        if not c: raise HTTPException(404, "Category not found")
        db.delete(c); db.commit()
        return {"ok": True}
    finally:
        db.close()

# ── LISTAS: TMDB Search ──────────────────────────────────────────────────

@app.get("/api/listas/tmdb-search")
async def tmdb_search(q: str = Query("", description="Search term"), page: int = Query(1, ge=1)):
    key = _get_tmdb_key()
    if not key:
        return {"results": [], "error": "TMDB_API_KEY no configurada. Agregala en /root/.hermes/.env o variable de entorno."}
    if not q.strip():
        return {"results": [], "error": "Query parameter 'q' is required"}
    try:
        url = f"https://api.themoviedb.org/3/search/multi?query={urllib.parse.quote(q)}&page={page}&language=es-ES"
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {key}",
            "Accept": "application/json"
        })
        ctx = ssl._create_unverified_context()
        r = urllib.request.urlopen(req, timeout=10, context=ctx)
        data = json.loads(r.read())
        results = []
        for item in data.get("results", []):
            media_type = item.get("media_type", "movie")
            title = item.get("title") or item.get("name", "")
            release = item.get("release_date") or item.get("first_air_date", "")
            poster = item.get("poster_path", "")
            results.append({
                "id": item["id"],
                "title": title,
                "type": media_type,
                "overview": (item.get("overview") or "")[:300],
                "release_date": release,
                "poster_path": poster,
                "poster_url": f"https://image.tmdb.org/t/p/w500{poster}" if poster else None,
                "vote_average": item.get("vote_average", 0)
            })
        return {"results": results, "total_pages": data.get("total_pages", 1), "total_results": data.get("total_results", 0)}
    except Exception as ex:
        return {"results": [], "error": str(ex)[:200]}

# ═══════════════════════════════════════════════════════════════════════════
# ── AKIRA INFO (Hermes status) ───────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════

@app.get("/api/akira/info")
async def akira_info():
    info = {}

    # 1. Hermes status subprocess
    try:
        r = subprocess.run(["/usr/local/lib/hermes-agent/venv/bin/hermes", "status"],
            capture_output=True, text=True, timeout=15)
        info["hermes_status"] = r.stdout.strip()[:2000]
        if r.stderr.strip():
            info["hermes_status_stderr"] = r.stderr.strip()[:500]
    except Exception as ex:
        info["hermes_status"] = f"Error: {str(ex)[:200]}"

    # 2. Skills list
    try:
        r = subprocess.run(["/usr/local/lib/hermes-agent/venv/bin/hermes", "skills", "list"],
            capture_output=True, text=True, timeout=15)
        info["available_skills"] = r.stdout.strip()[:3000]
        if r.stderr.strip():
            info["skills_stderr"] = r.stderr.strip()[:500]
    except Exception as ex:
        info["available_skills"] = f"Error: {str(ex)[:200]}"

    # 3. Config: model, provider, enabled skills
    try:
        config_path = Path("/root/.hermes/config.yaml")
        if config_path.exists():
            raw = config_path.read_text()
            # Extract model and provider
            model_match = re.search(r'^\s*default:\s*(\S+)', raw, re.MULTILINE)
            provider_match = re.search(r'^\s*provider:\s*(\S+)', raw, re.MULTILINE)
            info["config_model"] = model_match.group(1) if model_match else "unknown"
            info["config_provider"] = provider_match.group(1) if provider_match else "unknown"
            # Extract skills from config
            skills = []
            for line in raw.split("\n"):
                line_s = line.strip()
                if line_s.startswith("- ") and not any(x in line_s for x in ["/", "{{", "{%"]):
                    s = line_s[2:].strip()
                    if s and not s.startswith("#"):
                        skills.append(s)
            info["config_skills_raw"] = skills[:30]
        else:
            info["config_error"] = "config.yaml not found"
    except Exception as ex:
        info["config_error"] = str(ex)[:200]

    # 4. Profile skills directory listing
    try:
        profiles_dir = Path.home() / ".hermes" / "profiles"
        current_profile = "default"
        profiles = []
        if profiles_dir.exists():
            profiles = [p.name for p in profiles_dir.iterdir() if p.is_dir()]
        info["profiles"] = profiles
        info["current_profile"] = current_profile
        # List skills of current default profile
        skills_dir_home = Path.home() / ".hermes" / "skills"
        profile_skills = []
        if skills_dir_home.exists():
            profile_skills = sorted([p.name for p in skills_dir_home.iterdir() if p.is_dir() or p.is_file()])
        info["profile_skills_dir"] = profile_skills[:30]
    except Exception as ex:
        info["profile_skills_error"] = str(ex)[:200]

    return info

# ═══════════════════════════════════════════════════════════════════════════
static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8585))
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
