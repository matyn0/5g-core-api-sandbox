from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data import fake_ue_data
from app.database import SubscriptionRecord, get_db
from app.models import SubscriptionRequest


router = APIRouter()


# Convert an internal database ID such as 1 into the public API ID "sub-001".
def _format_subscription_id(record_id: int) -> str:
    return f"sub-{record_id:03}"


# Convert a database subscription object into the JSON structure
# expected by API clients.
def _subscription_to_dict(record: SubscriptionRecord) -> dict:
    return {
        "subscription_id": _format_subscription_id(record.id),
        "ue_id": record.ue_id,
        "event_type": record.event_type,
        "callback_url": record.callback_url,
        "status": record.status,
    }


# Convert a public subscription ID such as "sub-001" into database ID 1.
# Invalid formats are reported as missing subscriptions.
def _parse_subscription_id(subscription_id: str) -> int:
    if not subscription_id.startswith("sub-"):
        raise HTTPException(
            status_code=404,
            detail="Subscription not found",
        )

    raw_id = subscription_id.removeprefix("sub-")

    if not raw_id.isdigit():
        raise HTTPException(
            status_code=404,
            detail="Subscription not found",
        )

    record_id = int(raw_id)

    # Require the same ID format produced by the API.
    # For example, "sub-1" is rejected because the API uses "sub-001".
    if _format_subscription_id(record_id) != subscription_id:
        raise HTTPException(
            status_code=404,
            detail="Subscription not found",
        )

    return record_id


# Find one subscription in the database or return HTTP 404.
def _get_subscription_record(
    database: Session,
    subscription_id: str,
) -> SubscriptionRecord:
    record_id = _parse_subscription_id(subscription_id)
    record = database.get(SubscriptionRecord, record_id)

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Subscription not found",
        )

    return record


@router.get("/nef/ue")
def list_ues():
    # UE data remains static simulator data for now.
    return {
        "count": len(fake_ue_data),
        "ues": list(fake_ue_data.values()),
    }


@router.get("/nef/ue/{ue_id}/status")
def get_ue_status(ue_id: str):
    if ue_id not in fake_ue_data:
        raise HTTPException(
            status_code=404,
            detail="UE not found",
        )

    return fake_ue_data[ue_id]


@router.post("/nef/subscriptions")
def create_subscription(
    subscription: SubscriptionRequest,
    database: Session = Depends(get_db),
):
    # Subscriptions may only reference known simulated UEs.
    if subscription.ue_id not in fake_ue_data:
        raise HTTPException(
            status_code=404,
            detail="UE not found",
        )

    # Build a new database record from the validated request.
    record = SubscriptionRecord(
        ue_id=subscription.ue_id,
        event_type=subscription.event_type,
        callback_url=subscription.callback_url,
        status="active",
    )

    # Add the record, save the transaction, and load its generated ID.
    database.add(record)
    database.commit()
    database.refresh(record)

    return _subscription_to_dict(record)


@router.get("/nef/subscriptions")
def list_subscriptions(
    database: Session = Depends(get_db),
):
    # Return subscriptions in ID order for predictable API responses.
    statement = select(SubscriptionRecord).order_by(
        SubscriptionRecord.id
    )
    records = database.scalars(statement).all()

    return {
        "count": len(records),
        "subscriptions": [
            _subscription_to_dict(record)
            for record in records
        ],
    }


@router.get("/nef/subscriptions/{subscription_id}")
def get_subscription(
    subscription_id: str,
    database: Session = Depends(get_db),
):
    record = _get_subscription_record(
        database,
        subscription_id,
    )

    return _subscription_to_dict(record)


@router.delete("/nef/subscriptions/{subscription_id}")
def delete_subscription(
    subscription_id: str,
    database: Session = Depends(get_db),
):
    record = _get_subscription_record(
        database,
        subscription_id,
    )

    # Prepare the response before deleting the database object.
    deleted_subscription = _subscription_to_dict(record)

    database.delete(record)
    database.commit()

    return {
        "message": "Subscription deleted",
        "subscription": deleted_subscription,
    }