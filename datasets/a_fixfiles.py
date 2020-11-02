
"""
Simple helper file to fix the XML files from the dataset.
All `la******` files must be at the same level as this file.
What it does for each LA file:
- Retrieve the content
- Create a new file with same filename + ".xml"
- Write the content with an additional custom XML root node
"""

import os
from os import path
import re

PATTERN = re.compile(r"la[0-9]{6}")
files = [
    file for file in os.listdir(path.dirname(path.abspath(__file__)))
    if path.isfile(file) and PATTERN.match(file)
]
print(files)

for file in files:
    with open(file, mode="r") as file_read:
        content = file_read.read()

    with open(f"{file}.xml", mode="w") as file_write:
        file_write.write(f"<customroot>{content}</customroot>")
