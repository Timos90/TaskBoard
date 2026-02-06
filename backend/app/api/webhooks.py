""" 
Webhook Handlers - Listens to events from Clerk (subscription changes)

This file handles subscription webhooks from Clerk to automatically adjust
organization member limits based on their subscription tier:
- Free tier: Limited to 2 members
- Pro tier: Unlimited members (set to 1,000,000)

When a subscription is created/updated/cancelled, this webhook updates
the organization's max_allowed_memberships in Clerk.
"""

import json
from fastapi import APIRouter, Request, HTTPException, status
from svix.webhooks import Webhook, WebhookVerificationError
from app.core.config import settings
from app.core.clerk import clerk

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])

# Subscription tier configuration
PRO_TIER_SLUG = "pro_tier"  # The slug name for pro subscription in Clerk
FREE_TIER_LIMIT = settings.FREE_TIER_LIMIT  # Max members for free tier (2)
UNLIMITED_LIMIT = 1000000  # Effectively unlimited members for pro tier


def set_org_member_limit(org_id: str, limit: int):
    """ 
    Updates the maximum allowed members for an organization in Clerk
    
    Args:
        org_id: The Clerk organization ID
        limit: Maximum number of members allowed
    """
    clerk.organizations.update(
        organization_id=org_id,
        max_allowed_memberships=limit
    )


def has_active_pro_plan(items: list) -> bool:
    """ 
    Checks if the subscription has an active pro plan
    
    Args:
        items: List of subscription items from Clerk webhook data
    
    Returns:
        True if any item is an active pro tier subscription
    """
    return any(
        item.get("plan", {}).get("slug") == PRO_TIER_SLUG
        and item.get("status") == "active"
        for item in items
    )


@router.post("/clerk")
async def clerk_webhook(request: Request):
    """ 
    Handles webhook events from Clerk for subscription changes
    
    Listens for:
    - subscription.created: New subscription started
    - subscription.updated: Subscription plan changed
    - subscription.deleted: Subscription removed
    - subscription.cancelled: Subscription cancelled
    
    Automatically adjusts organization member limits based on subscription tier.
    """
    payload = await request.body()
    headers = dict(request.headers)

    # Verify webhook signature if secret is configured (recommended for production)
    if settings.CLERK_WEBHOOK_SECRET:
        try:
            wh = Webhook(settings.CLERK_WEBHOOK_SECRET)
            event = wh.verify(payload, headers)
        except WebhookVerificationError:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid signature")
    else:
        # Development mode: skip verification (not recommended for production)
        event = json.loads(payload)

    event_type = event.get("type")
    data = event.get("data", {})

    # Handle subscription creation or updates
    if event_type in ["subscription.created", "subscription.updated"]:
        org_id = data.get("payer", {}).get("organization_id")
        if org_id:
            # Set unlimited members for pro tier, otherwise use free tier limit
            limit = (UNLIMITED_LIMIT if has_active_pro_plan(data.get("items", []))
                     else FREE_TIER_LIMIT)
            set_org_member_limit(org_id, limit)
    
    # Handle subscription deletion or cancellation
    elif event_type in ["subscription.deleted", "subscription.cancelled"]:
        org_id = data.get("payer", {}).get("organization_id")
        if org_id:
            # Revert to free tier limits when subscription ends
            set_org_member_limit(org_id, FREE_TIER_LIMIT)

    return {"received": True}