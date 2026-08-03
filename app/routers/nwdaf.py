from fastapi import APIRouter, HTTPException

from app.data import fake_slice_load_data

router = APIRouter()


@router.get("/nwdaf/analytics/slice-load")
def get_slice_load_analytics():
    return {
        "analytics_type": "slice-load",
        "slices": list(fake_slice_load_data.values()),
    }


@router.get("/nwdaf/analytics/slice-load/{slice_id}")
def get_slice_load_analytics_by_slice(slice_id: str):
    if slice_id not in fake_slice_load_data:
        raise HTTPException(status_code=404, detail="Slice not found")

    return {
        "analytics_type": "slice-load",
        "slice": fake_slice_load_data[slice_id],
    }
