#!/usr/bin/env python3

import sys

import ruamel.yaml
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab import platypus
from reportlab.lib.styles import getSampleStyleSheet
import datetime

pdfmetrics.registerFont(TTFont('dejavu-sans', '/usr/share/fonts/truetype/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('dejavu-sans-bold', '/usr/share/fonts/truetype/DejaVuSans-Bold.ttf'))

paragraph = ParagraphStyle(name="Text", fontName="dejavu-sans", fontSize=8)
headline = ParagraphStyle(name="Headline", fontName="dejavu-sans-bold")

class Resume:
    def __init__(self, source, target):
        # get data
        yaml = ruamel.yaml.YAML()
        with open(source) as stream:
            self.data = yaml.load(stream)
        # start document
        self.doc = platypus.SimpleDocTemplate(target)
        # items
        self.items = []

    def add(self, item, style=paragraph):
        if isinstance(item, str):
            item = platypus.Paragraph(item, style=style)
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
            self.add(f"{work['position']}", style=headline)
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
        self.add(platypus.FrameBreak())
        for skill in self.data['skills']:
            self.add(f"{skill['name']}", style=headline)
            self.add(f"{skill['detail']}")
            level = round(skill['level'] * 10)
            self.add("\u25cf" * level + "\u25cb" * (10-level))
            self.add("\xa0")
        self.add(f"{self.data['notice']}")

        self.doc.addPageTemplates([platypus.PageTemplate(id='resume', frames=[
            platypus.Frame(self.doc.leftMargin, self.doc.bottomMargin, self.doc.width/2-6, self.doc.height, id='left'),
            platypus.Frame(self.doc.leftMargin + self.doc.width/2+6, self.doc.bottomMargin, self.doc.width/2-6, self.doc.height, id='right'),
        ])])
        self.doc.build([platypus.NextPageTemplate('resume')] + self.items)

if __name__ == '__main__':
    resume = Resume(*sys.argv[1:])
    resume.build()
