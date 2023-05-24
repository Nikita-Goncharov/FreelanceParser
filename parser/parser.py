import os
import requests

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import emoji
from reloading import reloading
from telegram.ext import Updater

updater = Updater(os.getenv("BOT_TOKEN"))

load_dotenv()


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

prev_last_task_time = 0


@reloading
def make_string_message(task_tr_tag):
    left_section = task_tr_tag.findChild('td', attrs={'class': 'left'})
    project_budget_section = task_tr_tag.findChild('td', attrs={'class': 'project-budget'})
    project_budget = "--"
    budget_div = None
    premium_label = f"{emoji.emojize('⭐')}Premium Task\n\n" if left_section.findChild('span', attrs={'class': 'label color-orange with-tooltip'}) else f"{emoji.emojize('❗')}Task\n\n"

    if project_budget_section is not None:
        budget_div = project_budget_section.findChild('div', attrs={'class': 'text-green price with-tooltip'})
    else:
        budget_div = left_section.findChild('div', attrs={'class': 'text-green price with-tooltip'})

    if budget_div is not None:
        project_budget = budget_div.getText().replace("\n", "")

    a_tag = left_section.findChild('a', attrs={'class': 'visitable'})
    title = a_tag.getText().replace("\n", "")
    description = left_section.findChild('p').getText().replace("\n", "")
    task_link = a_tag['href']

    stringed_task = f"""{premium_label}{emoji.emojize('🏷')} Title: {title}\n\n{emoji.emojize('📑')} Description: {description}\n\n{emoji.emojize('💰')} Price: {project_budget}\n\nLink:{task_link}"""
    return stringed_task


def get_new_tasks(parsed_trs, last_task_time):
    new_tasks = []
    for tr in parsed_trs:
        if int(tr["data-published"]) > last_task_time:
            new_tasks.append(make_string_message(tr))

    if new_tasks:
        return new_tasks

    return None


def parse_freelancehunt():
    urls = {"javascript": "https://freelancehunt.com/ua/projects/skill/javascript/28.html", "python": "https://freelancehunt.com/ua/projects/skill/python/22.html"}

    global prev_last_task_time
    for url in urls.items():
        current_tasks_time = 0

        response = requests.get(url[1], headers=headers)

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find(class_='table table-normal project-list')
        parsed_trs = table.findChildren('tr')

        for tr in parsed_trs:
            if int(tr["data-published"]) > current_tasks_time:
                current_tasks_time = int(tr["data-published"])

        if prev_last_task_time != 0 and prev_last_task_time < current_tasks_time:
            stringed_tasks = get_new_tasks(parsed_trs, prev_last_task_time)
            if stringed_tasks:
                for task in stringed_tasks:
                    task = f"{url[0].capitalize()}/n{task}"
                    updater.bot.send_message(chat_id=os.getenv('CHAT_ID'), text=task)
            else:
                updater.bot.send_message(chat_id=os.getenv('CHAT_ID'), text="Error that should not occur")
        prev_last_task_time = current_tasks_time

