# Service Recovery Template

Add this section to your project's `NEXT_SESSION.md` or `docs/SESSION_DIARY.md` for any project that runs background services.

---

## Service Recovery

When recovering from a crash or starting fresh:

### 1. Check Service Status
```bash
# Check what's running
pgrep -fl "[project-name]"

# Check specific services
pgrep -fl "python.*main.py"
pgrep -fl "node.*server"
```

### 2. Start Services (if not running)
```bash
cd /path/to/your/project
source .venv/bin/activate  # if Python

# Start in dependency order:

# 1. External dependencies (databases, message queues, gateways)
# Example: redis-server &
# Example: python gateway.py &

# 2. Main application
# Example: python main.py >> logs/main.log 2>&1 &

# 3. Auxiliary services (dashboards, monitors, workers)
# Example: python dashboard.py >> logs/dashboard.log 2>&1 &
```

### 3. Verify Running
```bash
# Check logs
tail -f logs/*.log

# Health check
curl -s localhost:8000/health

# Process check
ps aux | grep "[p]roject-name"
```

### 4. Common Issues

| Issue | Check | Fix |
|-------|-------|-----|
| Service won't start | `tail logs/error.log` | Fix error and restart |
| Port already in use | `lsof -i :8000` | `kill <PID>` then restart |
| Missing environment | `cat .env` | Copy from `.env.example` |
| Stale PID file | `cat *.pid` | Remove if process not running |
| DB connection failed | Check DB is running | Start DB first |

---

## Usage

1. Copy the "Service Recovery" section above
2. Paste it into your project's `docs/NEXT_SESSION.md`
3. Customize the commands for your specific services
4. Now `/recover` will find and use these instructions
