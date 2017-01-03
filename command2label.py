#!/usr/bin/env python
'''
Command to Label

Usage: command2label <command>...
'''


import re
import sys
from docopt import docopt

args = docopt(__doc__)

commaAndNewlineRe = re.compile(r',\n\s*')
justNewlineRe = re.compile(r'\n\s*')
labelList = []
for commandFile in args.get('<command>', []):
    with open(commandFile) as f:
        multiLineCommand = f.read()
    singleLineCommand = commaAndNewlineRe.sub(', ', multiLineCommand)
    singleLineCommand = justNewlineRe.sub('', singleLineCommand)
    singleLineCommand = singleLineCommand.replace('"', r'\"')
    labelList.append(singleLineCommand)

print '"[{}]"'.format(', \\\n\t'.join(labelList))