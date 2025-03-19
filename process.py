# process raw.txt into json

import re
import json

# Read the raw text from a file
with open("raw.txt", "r", encoding="utf-8") as file:
    raw_text = file.read()

# Prepare an empty list for storing parsed idioms
idioms_list = []

# Split the raw text into lines for processing.
lines = raw_text.splitlines()

# Initialize a variable to store the current chapter source.
current_chapter = None

# Use index iteration so that we can look ahead for the example line.
i = 0
while i < len(lines):
    line = lines[i].strip()
    
    # Check if the line is a chapter header.
    chapter_match = re.match(r"\*\*Chapter\s+(\d+):", line)
    if chapter_match:
        # Set current chapter (e.g., "chapter 1")
        current_chapter = f"chapter {chapter_match.group(1)}"
        i += 1
        continue

    # Check if the line is an idiom line.
    idiom_match = re.match(r"\*\s+\*\*(.+?)\*\*:\s*(.+)", line)
    if idiom_match:
        idiom_text = idiom_match.group(1).strip()
        definition = idiom_match.group(2).strip()
        example = ""
        # Look ahead for the example line which is expected to start with an indented bullet.
        if i + 1 < len(lines):
            next_line = lines[i+1].strip()
            # Check if the next line is an example line (starts with a bullet marker)
            if next_line.startswith("*") or next_line.startswith("-"):
                # Remove the leading bullet marker.
                example = re.sub(r"^\*\s+", "", next_line).strip()
                i += 1  # Skip the example line in the next iteration.
        idioms_list.append({
            "idiom": idiom_text,
            "source": current_chapter,
            "definition": definition,
            "example": example
        })
    i += 1

# Write the JSON formatted result to a file.
with open("idioms.json", "w", encoding="utf-8") as outfile:
    json.dump(idioms_list, outfile, indent=4)

print("JSON output written to output.json")