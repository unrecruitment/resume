#!/usr/bin/env python3

import subprocess

import ruamel.yaml
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

class Resume:
    def __init__(self, name):
        # get data
        yaml = ruamel.yaml.YAML()
        with open(f"data/{name}.yaml") as stream:
            self.data = yaml.load(stream)
        # start document
        self.output = f"output/{name}.pdf"
        self.doc = SimpleDocTemplate(self.output)
        # items
        self.items = []

    def add(self, item, style=getSampleStyleSheet()['Normal']):
        if isinstance(item, str):
            item = Paragraph(item, style=style)
        self.items.append(item)


    def build(self):
        self.add(f"{self.data['name']}")
        self.add(f"{self.data['headline']}")
        self.add(f"{self.data['email']['username']}@{self.data['email']['domain']}")
        self.add(f"{self.data['homepage']}")
        for p in self.data['summary']:
            self.add(p)
        for work in self.data['experience']:
            self.add(f"{work['position']}")
            if 'from' in work:
                self.add(f"{work['from']}")
                self.add(f"{work.get('to', 'now')}")
            if 'description' in work:
                self.add(f"{work['description']}")
        for item in self.data['volunteering']:
            self.add(f"{item}")
        for skill in self.data['skills']:
            self.add(f"{skill['name']}")
            self.add(f"{skill['detail']}")
            self.add(f"{skill['level']}")
        self.add(f"{self.data['notice']}")
        self.doc.build(self.items)

if __name__ == '__main__':
    resume = Resume('pavelsimerda')
    resume.build()
    subprocess.run(['xdg-open', resume.output])
