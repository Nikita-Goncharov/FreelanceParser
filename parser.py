import os
import asyncio
from httpx import AsyncClient
import emoji
from datetime import datetime
from telegram import Bot
from dotenv import load_dotenv


load_dotenv()

API_TOKEN = os.getenv("FREELANCEHUNT_API_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

ids = os.getenv("CHAT_IDS")
CHAT_IDS = [int(str_id) for str_id in ids.split(",")]

bot = Bot(TELEGRAM_TOKEN)

SKILLS = [
    {"id": 175, "name": "AI & Machine Learning"},
    {"id": 22, "name": "Python"},
    {"id": 86, "name": "Databases & SQL"},
    {"id": 99, "name": "Web Programming"},
    {"id": 96, "name": "Website Development"},
    {"id": 45, "name": "Website Maintenance"},
    {"id": 180, "name": "Bot Development"},
    {"id": 42, "name": "Interface Design (UI\/UX)"},
    {"id": 43, "name": "Web Design"},
    {"id": 179, "name": "Mobile Apps Design"},
    {"id": 190, "name": "AI Consulting"},
    {"id": 183, "name": "Hybrid Mobile Apps"},
    {"id": 124, "name": "HTML & CSS"},
    {"id": 28, "name": "Javascript and Typescript"},

    {"id": 185, "name": "AR & VR Development"},
    {"id": 2, "name": "C & C++"},
    {"id": 24, "name": "C#"},
    {"id": 108, "name": "Architectural Design"},
    {"id": 182, "name": "Cryptocurrency & Blockchain"},
    {"id": 65, "name": "Cybersecurity & Data Protection"},
    {"id": 169, "name": "Data Parsing"},
    {"id": 178, "name": "Data Processing"},
    {"id": 103, "name": "Desktop Apps"},
    {"id": 181, "name": "DevOps"},
    {"id": 176, "name": "Embedded Systems & Microcontrollers"},
    {"id": 148, "name": "Engineering"},
    {"id": 6, "name": "Linux & Unix"},
    {"id": 188, "name": "Mechanical Engineering & Instrument Making"},
    {"id": 129, "name": "Payment Systems Integration"},
    {"id": 163, "name": "Script Writing"},
    {"id": 83, "name": "Software & Server Configuration"},
    {"id": 157, "name": "Software, Website & Game Localization"},
    {"id": 39, "name": "System & Network Administration"},
    {"id": 97, "name": "Technical Documentation"},
    {"id": 57, "name": "Testing & QA"}
]

last_published = None

async_client = AsyncClient()

async def fetch_projects():
    url = "https://api.freelancehunt.com/v2/projects"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Accept": "application/json",
    }

    resp = await async_client.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()["data"]


def format_message(project, skills):
    attrs = project["attributes"]
    budget = attrs.get("budget")
    price = f"{budget['amount']} {budget['currency']}" if budget else "--"

    is_premium = attrs.get("is_premium", False)
    premium_label = f"{emoji.emojize('⭐')} Premium Task\n\n" if is_premium else f"{emoji.emojize('❗')} Task\n\n"

    skills_pretty = ", ".join([skill["name"] for skill in skills])

    return (
        f"{premium_label}"
        f"Categories: {skills_pretty}\n"
        f"{emoji.emojize('🏷')} Title: {attrs['name']}\n\n"
        f"{emoji.emojize('📑')} Description: {attrs['description']}\n\n"
        f"{emoji.emojize('💰')} Price: {price}\n\n"
        f"🔗 Link: {project['links']['self']['web']}"
    )


async def process_projects():
    global last_published
    projects = await fetch_projects()
    
    if last_published is None:
        last_project = projects[0]
        attrs = last_project["attributes"]
        last_published = datetime.fromisoformat(attrs["published_at"].replace("Z", "+00:00"))
        return 
    
    # from old to new
    projects = projects[::-1]

    for prj in projects:
        attrs = prj["attributes"]
        project_skills_ids = [skill["id"] for skill in attrs.get("skills", [])]
        published = datetime.fromisoformat(attrs["published_at"].replace("Z", "+00:00"))

        if published > last_published:
            # matching skills by ids 
            matched_skills = [skill for skill in SKILLS if skill["id"] in project_skills_ids]
            if not matched_skills:
                continue
            msg = format_message(prj, matched_skills)
            print("New project found")
            for chat_id in CHAT_IDS:
                print("Sending messages")
                await bot.send_message(chat_id=chat_id, text=msg)
            last_published = published


async def main():
    while True:
        try:
            await process_projects()
        except Exception as e:
            print(f"Error: {e}, type: {type(e)}")
        await asyncio.sleep(10)
        print("Next cycle")


if __name__ == "__main__":
    asyncio.run(main())
