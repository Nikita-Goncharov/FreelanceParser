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
CHAT_IDS = map(lambda str_id: int(str_id), ids.split(","))

bot = Bot(TELEGRAM_TOKEN)

CATEGORIES = [
    "3D Modeling",
    "Accounting Services",
    "Advertising",
    "AI & Machine Learning",
    "AI Art",
    "AI Consulting",
    "AI Content Creation",
    "AI Speech & Audio Generation",
    "Animation",
    "App Development for Android",
    "App Store Optimization (ASO)",
    "Apps for iOS (iPhone and iPad)",
    "AR & VR Development",
    "Architectural Design",
    "Articles & Blog Posts",
    "Artwork",
    "Audio & Video Editing",
    "Audio Processing",
    "Banners",
    "Bot Development",
    "Business Card Design",
    "C & C++",
    "C#",
    "Client Management & CRM",
    "Clothing design",
    "Consulting",
    "Content Management",
    "Content Management Systems",
    "Contextual Advertising",
    "Copywriting",
    "Corporate Style",
    "Cryptocurrency & Blockchain",
    "Customer Support",
    "Cybersecurity & Data Protection",
    "Data Parsing",
    "Data Processing",
    "Databases & SQL",
    "Desktop Apps",
    "DevOps",
    "Drawings & Diagrams",
    "Email Marketing",
    "Embedded Systems & Microcontrollers",
    "Engineering",
    "English",
    "Enterprise Resource Planning (ERP)",
    "Exhibition Booth Design",
    "French",
    "Gaming Apps",
    "German",
    "HTML & CSS",
    "Hybrid Mobile Apps",
    "Icons & Pixel Graphics",
    "Illustrations & Drawings",
    "Industrial Design",
    "Infographics",
    "Information Gathering",
    "Interface Design (UI/UX)",
    "Interior Design",
    "Java",
    "Javascript and Typescript",
    "Landscape Projects & Design",
    "Lead Generation & Sales",
    "Legal Services",
    "Link Building",
    "Linux & Unix",
    "Logo Design",
    "Marketing Research",
    "Mechanical Engineering & Instrument Making",
    "Mobile Apps Design",
    "Music",
    "Naming & Slogans",
    "Object Design",
    "Online Stores & E-commerce",
    "Outdoor Advertising",
    "Packaging and label design",
    "Payment Systems Integration",
    "Photo Processing",
    "Photography",
    "PHP",
    "Poems, Songs & Prose",
    "Polish",
    "Presentations",
    "Print Design",
    "Project Management",
    "Public Relations (PR)",
    "Python",
    "Recruitment (HR)",
    "Rewriting",
    "Script Writing",
    "Search Engine Optimization (SEO)",
    "Search Engine Reputation Management (SERM)",
    "Social Media Advertising",
    "Social Media Marketing (SMM)",
    "Social Media Page Design",
    "Software & Server Configuration",
    "Software, Website & Game Localization",
    "Spanish",
    "Speaker & Voice Services",
    "System & Network Administration",
    "Teaser Advertisements",
    "Technical Documentation",
    "Testing & QA",
    "Text Editing & Proofreading",
    "Text Translation",
    "Transcribing",
    "Tuition",
    "Type & Font Design",
    "Ukrainian",
    "Vector Graphics",
    "Video Advertising",
    "Video Creation by Artificial Intelligence",
    "Video Processing",
    "Video Recording",
    "VR & AR Design",
    "Web Design",
    "Web Programming",
    "Website Development",
    "Website Maintenance",
    "Website SEO Audit",
    "Windows",
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


def format_message(project, categories):
    attrs = project["attributes"]
    budget = attrs.get("budget")
    price = f"{budget['amount']} {budget['currency']}" if budget else "--"

    is_premium = attrs.get("is_premium", False)
    premium_label = f"{emoji.emojize('⭐')} Premium Task\n\n" if is_premium else f"{emoji.emojize('❗')} Task\n\n"

    categories_pretty = ", ".join([c for c in categories])

    return (
        f"{premium_label}"
        f"Categories: {categories_pretty}\n"
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
        skills = [s["name"] for s in attrs.get("skills", [])]
        published = datetime.fromisoformat(attrs["published_at"].replace("Z", "+00:00"))

        # matched_cats = [c for c in CATEGORIES if c in skills]
        # if not matched_cats:
        #     continue

        if published > last_published:
            msg = format_message(prj, skills)
            for chat_id in CHAT_IDS:
                await bot.send_message(chat_id=chat_id, text=msg)
            last_published = published

async def main():
    while True:
        try:
            await process_projects()
        except Exception as e:
            print(f"Error: {e}, type: {type(e)}")
        await asyncio.sleep(30)
        print("Next cycle")

if __name__ == "__main__":
    asyncio.run(main())
