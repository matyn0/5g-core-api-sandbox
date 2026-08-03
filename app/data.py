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
