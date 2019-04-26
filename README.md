### Required API scope
```
scope=offline,photos,wall,groups
```

### Run locally in test mode
```bash
uvicorn app.main:app
```

### Run in life mode
```bash
sudo /../.venv/name/bin/uvicorn app.main:app --host 0.0.0.0 --port 80
```

Use `--lifespan on` to check that everything ok with startup hooks