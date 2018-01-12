#!/usr/bin/env python

"""
Convert Slicer executable XML into XNAT command

Usage:
    slicerxml2command.py [--debug] [--docker-image IMAGE] [--path-to-slicer PATH_TO_SLICER] --input SLICER_XML_FILE --output COMMAND_JSON_FILE
    slicerxml2command.py --help | --version

Options:
    -d IMAGE, --docker-image IMAGE                      Docker image for the command. [default: slicer]
    -p PATH_TO_SLICER, --path-to-slicer PATH_TO_SLICER  Path to slicer executable within image [default: /opt/slicer/Slicer]
    -i SLICER_XML_FILE, --input SLICER_XML_FILE         Input file: Slicer XML.
    -o COMMAND_JSON_FILE, --output COMMAND_JSON_FILE    Output file: command JSON.
    --debug                                             Turn on debug print statements
    --help                                              Show this help message and exit
    --version                                           Show version and exit
"""

__version__ = "1"
__author__ = "Flavin"


import os
import sys
import json
from lxml import etree
from docopt import docopt

def xpathOrDefault(node, path, default=""):
    return node.xpath(path)[0].text if node.xpath(path) else default

args = docopt(__doc__, version=__version__)
image = args["--docker-image"]
slicerPath = args["--path-to-slicer"]
slicerXmlFilePath = args["--input"]
commandJsonFilePath = args["--output"]
debug = args["--debug"]

slicerXmlFile = os.path.basename(slicerXmlFilePath)
slicerExecutableName = os.path.splitext(slicerXmlFile)[0]

root = etree.parse(slicerXmlFilePath)

title = root.xpath("/executable/title")
if not title or not title[0].text:
    message = "ERROR: Could not find executable's title. Generated Command would be invalid."
    if debug:
        print(message)
    sys.exit(message)

if debug:
    print("Finding parameters.")
parameters = []
for parametersBlock in root.xpath("/executable/parameters"):
    # There can be several <parameters> blocks in the document.
    # Each <parameters> block will have its own <label> and <description>.
    # We skip them because we have no notion of grouping inputs.
    # Everything else is a parameter that we want.
    parameters += [child for child in parametersBlock.getchildren() \
                    if child.tag != "label" and child.tag != "description"]

if debug:
    print("Creating command inputs from parameters.")
commandInputs = []
commandInputsWithIndices = []
for param in parameters:

    name = param.xpath("./name")
    if not name or not name[0].text:
        if debug:
            print("Parameter has no name! Skipping.")
            print(param)
        continue

    if debug:
        print("Processing parameter \"{}\".".format(name[0].text))

    # We can't deal with "-vector" or "-enumeration" param types, so
    # for now we pretend they do not exist
    tag = param.tag if "-" not in param.tag else \
            param.tag[:param.tag.index("-")]
    inputType = "boolean" if tag == "boolean" else \
                "number" if tag in ("integer", "float", "double") else \
                "string"

    if debug:
        print("tag \"{}\" -> input type \"{}\".".format(tag, inputType))

    commandInput = {
        "name": name[0].text,
        "type": inputType,
        "description": xpathOrDefault(param, "./description"),
        "required": True,
        "default-value": xpathOrDefault(param, "./default")
    }

    longflag = xpathOrDefault(param, "./longflag")
    longflagWithDashes = "" if not longflag else \
                         longflag if longflag[:2] == "--" else \
                         "--" + longflag
    shortflag = xpathOrDefault(param, "./flag")
    shortflagWithDash = "" if not shortflag else \
                        shortflag if shortflag[0] == "-" else \
                        "-" + shortflag
    flag = longflagWithDashes if longflagWithDashes and inputType != "boolean" else \
           shortflagWithDash if shortflagWithDash and inputType != "boolean" else \
           ""
    trueValue = longflag if longflag and inputType == "boolean" else ""

    if inputType == "boolean":
        commandInput["true-value"] = trueValue
    elif flag:
        commandInput["command-line-flag"] = flag

    if debug:
        print("Input: {}".format(commandInput))

    index = xpathOrDefault(param, "./index", None)
    if index:
        commandInputsWithIndices.append((index, commandInput))
    else:
        commandInputs.append(commandInput)

commandLineParts = [slicerPath, "--launch", slicerExecutableName]
commandLineParts += ["#{}#".format(commandInput["name"]) for commandInput in commandInputs]
if commandInputsWithIndices:
    commandInputsWithIndices.sort(key=lambda t: t[0])  # Sort in place so it is still sorted when we use it later
    commandLineParts += ["#{}#".format(commandInput["name"]) for index, commandInput in commandInputsWithIndices]

if debug:
    print("Command-line parts:")
    print(commandLineParts)

if debug:
    print("Constructing command.")
command = {
    "name": title[0].text,
    "label": title[0].text,
    "description": xpathOrDefault(root, "/executable/description"),
    "version": xpathOrDefault(root, "/executable/version"),
    "info-url": xpathOrDefault(root, "/executable/documentation-url"),
    "schema-version": "1.0",
    "type": "docker",
    "image": image,
    "command-line": " ".join(commandLineParts),
    "inputs": commandInputs + [commandInput for index, commandInput in commandInputsWithIndices],
    "xnat": []
}

with open(commandJsonFilePath, 'w') as f:
    json.dump(command, f, indent=4, separators=(',', ': '))
