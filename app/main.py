from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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

fake_slice_load_data = {
    "slice-embb": {
        "slice_id": "slice-embb",
        "name": "Enhanced Mobile Broadband",
        "load_percent": 72,
        "active_ues": 128,
        "status": "high",
    },
    "slice-urllc": {
        "slice_id": "slice-urllc",
        "name": "Ultra-Reliable Low-Latency Communications",
        "load_percent": 34,
        "active_ues": 42,
        "status": "normal",
    },
    "slice-mmtc": {
        "slice_id": "slice-mmtc",
        "name": "Massive Machine-Type Communications",
        "load_percent": 18,
        "active_ues": 360,
        "status": "normal",
    },
}

fake_subscriptions = {}


class SubscriptionRequest(BaseModel):
    ue_id: str
    event_type: str
    callback_url: str






##### GET SECTION #######

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/nef/ue")
def list_ues():
    return {
        "count": len(fake_ue_data),
        "ues": list(fake_ue_data.values()),
    }

@app.get("/nwdaf/analytics/slice-load")
def get_slice_load_analytics():
    return {
        "analytics_type": "slice-load",
        "slices": list(fake_slice_load_data.values()),
    }

@app.get("/nef/ue/{ue_id}/status")
def get_ue_status(ue_id: str):
    if ue_id not in fake_ue_data:
        raise HTTPException(status_code=404, detail="UE not found")

    return fake_ue_data[ue_id]

@app.get("/nwdaf/analytics/slice-load/{slice_id}")
def get_slice_load_analytics_by_slice(slice_id: str):
    if slice_id not in fake_slice_load_data:
        raise HTTPException(status_code=404, detail="Slice not found")

    return {
        "analytics_type": "slice-load",
        "slice": fake_slice_load_data[slice_id],
    }




##### POST SECTION ######

@app.post("/nef/subscriptions")
def create_subscription(subscription: SubscriptionRequest):
    if subscription.ue_id not in fake_ue_data:
        raise HTTPException(status_code=404, detail="UE not found")

    subscription_id = f"sub-{len(fake_subscriptions) + 1:03}"

    fake_subscriptions[subscription_id] = {
        "subscription_id": subscription_id,
        "ue_id": subscription.ue_id,
        "event_type": subscription.event_type,
        "callback_url": subscription.callback_url,
        "status": "active",
    }

    return fake_subscriptions[subscription_id]


@app.get("/nef/subscriptions")
def list_subscriptions():
    return {
        "count": len(fake_subscriptions),
        "subscriptions": list(fake_subscriptions.values()),
    }
