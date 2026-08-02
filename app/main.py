from fastapi import FastAPI

app = FastAPI(
    title="5G Core API Sandbox",
    description="Sandbox for simulating 5G NEF and NWDAF APIs.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}
