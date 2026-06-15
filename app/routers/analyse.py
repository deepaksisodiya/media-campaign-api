import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from anthropic import Anthropic
from app.routers.campaigns import campaigns_db

load_dotenv()

router = APIRouter(prefix="/campaigns", tags=["analyse"])

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


@router.post("/{campaign_id}/analyse")
def analyse_campaign(campaign_id: int):
    if campaign_id not in campaigns_db:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    campaign = campaigns_db[campaign_id]

    prompt = f"""You are a media campaign analyst. Analyse this advertising campaign and provide insights.

    Campaign Details:
    - Name: {campaign.name}
    - Budget: ${campaign.budget:,.2f}
    - Channel: {campaign.channel}
    - Status: {"Active" if campaign.is_active else "Inactive"}

    Provide:
    1. Budget assessment (is this budget appropriate for the channel?)
    2. Channel recommendation (is this the right channel for this campaign?)
    3. Two specific actionable recommendations to improve performance
    Keep your response concise and practical."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "campaign_id": campaign_id,
        "campaign_name": campaign.name,
        "analyse": message.content[0].text
    }