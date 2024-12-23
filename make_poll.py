#!/usr/bin/env python3
import argparse
import yaml
import csv

def write_questions(fh, groups):
    writer = csv.DictWriter(fh,
        fieldnames=['Title', 'Questions Name', 'Questions Type', 'Answers'],
        quoting=csv.QUOTE_ALL,
    )
    writer.writeheader()
    for group in groups:
        writer.writerow({'Title': group['title']})
        for question in group['questions']:
            if question.get('multiple', False):
                multiple = True
            elif question.get('single', False):
                multiple = False
            else:
                raise Exception("need to specify single/multiple")
            writer.writerow({
                'Questions Name': question['text'],
                'Questions Type': 'multiple' if multiple else 'single',
            })
            for option in question['options']:
                writer.writerow({
                    'Answers': option
                })
            writer.writerow({})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=argparse.FileType('r'))
    parser.add_argument('output', type=argparse.FileType('w'))
    args = parser.parse_args()
    data = yaml.load(args.input, Loader=yaml.SafeLoader)
    write_questions(args.output, data)


# template from Zoom
"""Title,Questions Name,Questions Type,Answers
Polling1,,,
,How useful was this meeting?,multiple,
,,,Extremely useful
,,,Somewhat useful
,,,Not useful at all
,,,
,How useful was this course?,single,
,,,Extremely useful
,,,Somewhat useful
,,,Not useful at all
Polling2,,,
,How useful was this meeting?,multiple,
,,,Extremely useful
,,,Somewhat useful
,,,Not useful at all
,,,
,How useful was this course?,single,
,,,Extremely useful
,,,Somewhat useful
,,,Not useful at all
"""
