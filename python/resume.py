#!/usr/bin/env python3

import sys

import ruamel.yaml
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import datetime

class Resume:
    def __init__(self, source, target):
        # get data
        yaml = ruamel.yaml.YAML()
        with open(source) as stream:
            self.data = yaml.load(stream)
        # start document
        self.doc = SimpleDocTemplate(target)
        # items
        self.items = []

    def add(self, item, style=getSampleStyleSheet()['Normal']):
        if isinstance(item, str):
            item = Paragraph(item, style=style)
        self.items.append(item)


    def build(self):
        self.add(f"{self.data['name']}")
        self.add(f"{self.data['headline']}")
        if 'email' in self.data:
            self.add(f"{self.data['email']['username']}@{self.data['email']['domain']}")
        self.add(f"{self.data['homepage']}")
        self.add("\xa0")
        for p in self.data['summary'].split('\n\n'):
            self.add(p)
            self.add("\xa0")
        for work in self.data['experience']:
            self.add(f"{work['position']}")
            if 'from' in work:
                date_from = datetime.datetime.strptime(work['from'], '%Y-%m')
                date_from = date_from.date().strftime("%b %Y")
                if 'to' in work:
                    date_to = datetime.datetime.strptime(work['to'], '%Y-%m')
                    date_to = date_to.date().strftime("%b %Y")
                else:
                    date_to = 'now'
                self.add(f"({date_from} – {date_to})")
            if 'description' in work:
                self.add(f"{work['description']}")
            self.add("\xa0")
        for item in self.data['volunteering']:
            self.add(f"{item}")
            self.add("\xa0")
        for skill in self.data['skills']:
            self.add(f"{skill['name']}")
            self.add(f"{skill['detail']}")
            level = round(skill['level'] * 10)
            self.add("\u25cb" * level)
            self.add("\xa0")
        self.add(f"{self.data['notice']}")
        self.doc.build(self.items)

if __name__ == '__main__':
    resume = Resume(*sys.argv[1:])
    resume.build()
