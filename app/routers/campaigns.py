from fastapi import APIRouter, HTTPException
from app.models import Campaign

router = APIRouter(prefix="/campaigns", tags=["campaigns"])

campaigns_db: dict[int, Campaign] = {}

next_id: int = 1


@router.get("/", response_model=list[Campaign])
def get_all_campaigns():
    return list(campaigns_db.values())


@router.get("/{campaign_id}", response_model=Campaign)
def get_campaign(campaign_id: int):
    if campaign_id not in campaigns_db:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaigns_db[campaign_id]


@router.post("/", response_model=Campaign, status_code=201)
def create_campaign(campaign: Campaign):
    global next_id
    campaign.id = next_id
    campaigns_db[next_id] = campaign
    next_id += 1
    return campaign


@router.put("/{campaign_id}", response_model=Campaign)
def update_campaign(campaign_id: int, updated: Campaign):
    if campaign_id not in campaigns_db:
        raise HTTPException(status_code=404, detail="Campaign not found")
    updated.id = campaign_id
    campaigns_db[campaign_id] = updated
    return updated


@router.delete("/{campaign_id}", status_code=204)
def delete_campaign(campaign_id: int):
    if campaign_id not in campaigns_db:
        raise HTTPException(status_code=404, detail="Campaign not found")
    del campaigns_db[campaign_id]