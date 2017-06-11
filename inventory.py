import requests
import re

import unicodecsv
import os

SETS = {}

endpoint = 'https://api.magicthegathering.io/v1/sets'

for s in requests.get(endpoint).json()['sets']:
    SETS[s['code']] = s['name']


def generate_csv(sender, condition, lines):

    total = 0
    filename = 'inventory.csv'
    with open(filename, 'wb') as csvfile:
        writer = unicodecsv.DictWriter(csvfile, encoding='utf-8', fieldnames=['Add Qty', 'Condition', "Product Name", "Language", "Category"])
        writer.writeheader()

        for line in lines:
            total += 1
            r = re.compile('([0-9]*) (.*) \[([A-Z]{3})\]')
            if r.match(line):
                qty, name, set_abbr = r.findall(line)[0]

                writer.writerow({
                    'Add Qty': qty,
                    'Condition': condition,
                    "Product Name": name,
                    "Language": "English",
                    "Category": SETS.get(set_abbr, "Unknown")
                })

    if total == 0:
        return False

    response = requests.post("https://api.mailgun.net/v2/gamerz.inventory.cards/messages",
                             data={
                                'from': 'scryglass@gamerz.inventory.cards',
                                'to': sender,
                                'text': 'Upload the attached CSV via Crystal Commerce Mass Create',
                                'subject': "Inventory Update",
                             },
                             files=[("attachment", open(filename))],
                             auth=requests.auth.HTTPBasicAuth('api', os.environ.get("MAILGUN_KEY")))
    response.raise_for_status()
    return True
