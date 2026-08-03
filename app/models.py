from pydantic import BaseModel


class SubscriptionRequest(BaseModel):
    ue_id: str
    event_type: str
    callback_url: str
