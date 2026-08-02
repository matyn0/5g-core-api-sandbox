from fastapi import FastAPI

app = FastAPI(
    title="5G Core API Sandbox",
    description="Sandbox for simulating 5G NEF and NWDAF APIs.",
    version="0.1.0",
)

fake_ue_data = {
    "001": {
        "ue_id": "001",
        "status": "connected",
        "slice_id": "slice-embb",
        "cell_id": "cell-01",
    },
    "002": {
        "ue_id": "002",
        "status": "idle",
        "slice_id": "slice-urllc",
        "cell_id": "cell-02",
    },
    "003": {
        "ue_id": "003",
        "status": "disconnected",
        "slice_id": "slice-mmtc",
        "cell_id": "cell-03",
    },
}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/nef/ue/{ue_id}/status")
def get_ue_status(ue_id: str):
    if ue_id not in fake_ue_data:
        raise HTTPException(status_code=404, detail="UE not found")

    return fake_ue_data[ue_id]
