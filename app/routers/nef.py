from fastapi import APIRouter, HTTPException

from app.data import fake_subscriptions, fake_ue_data
from app.models import SubscriptionRequest

router = APIRouter()


@router.get("/nef/ue")
def list_ues():
    return {
        "count": len(fake_ue_data),
        "ues": list(fake_ue_data.values()),
    }


@router.get("/nef/ue/{ue_id}/status")
def get_ue_status(ue_id: str):
    if ue_id not in fake_ue_data:
        raise HTTPException(status_code=404, detail="UE not found")

    return fake_ue_data[ue_id]


@router.post("/nef/subscriptions")
def create_subscription(subscription: SubscriptionRequest):
    if subscription.ue_id not in fake_ue_data:
        raise HTTPException(status_code=404, detail="UE not found")

    next_subscription_number = max(
        (
            int(subscription_id.removeprefix("sub-"))
            for subscription_id in fake_subscriptions
        ),
        default=0,
    ) + 1
    subscription_id = f"sub-{next_subscription_number:03}"

    fake_subscriptions[subscription_id] = {
        "subscription_id": subscription_id,
        "ue_id": subscription.ue_id,
        "event_type": subscription.event_type,
        "callback_url": subscription.callback_url,
        "status": "active",
    }

    return fake_subscriptions[subscription_id]


@router.get("/nef/subscriptions")
def list_subscriptions():
    return {
        "count": len(fake_subscriptions),
        "subscriptions": list(fake_subscriptions.values()),
    }


@router.get("/nef/subscriptions/{subscription_id}")
def get_subscription(subscription_id: str):
    if subscription_id not in fake_subscriptions:
        raise HTTPException(status_code=404, detail="Subscription not found")

    return fake_subscriptions[subscription_id]


@router.delete("/nef/subscriptions/{subscription_id}")
def delete_subscription(subscription_id: str):
    if subscription_id not in fake_subscriptions:
        raise HTTPException(status_code=404, detail="Subscription not found")

    deleted_subscription = fake_subscriptions.pop(subscription_id)

    return {
        "message": "Subscription deleted",
        "subscription": deleted_subscription,
    }
