
import re
import sys
from typing import List

RANGE_SEPARATORS = "[-–—−]"  # hyphen, endash, emdash, minus
RANGE_REGEX = f"(\\d+\\s?{RANGE_SEPARATORS}\\s?\\d+\s)"
SINGLE_REGEX = "(\\d+\s)"
NUMBER_COLUMN_REGEX = f"^({RANGE_REGEX}|{SINGLE_REGEX})"

def convert(input: str) -> str:
    output_lines = []
    _add_header_footer(output_lines)

    for line in input.split("\n"):
        if _is_markdown(line):
            line = _markdown_to_plain(line)

        if _is_header(line):
            continue

        columns = _split_to_columns(line)
        for i in range(_extract_range(columns[0])):
            output_lines.append(columns[1])
    
    _add_header_footer(output_lines)

    return "\n".join(output_lines)

def _add_header_footer(output_lines):
    output_lines.extend(["", "---"])

def _is_markdown(line: str) -> bool:
    return line.startswith("|")

def _markdown_to_plain(line: str) -> str:
    return line[1:-1].replace("|", " ")

def _is_header(line: str) -> bool:
    return not re.search("^\\d", line)

def _split_to_columns(line: str) -> List[str]:
    m = re.search(NUMBER_COLUMN_REGEX, line)
    columns = [
        m.group(0).replace(" ", ""),
        line.replace(m.group(0), "").strip()
    ]
    return columns

def _extract_range(spec: str) -> int:
    if not re.search(RANGE_SEPARATORS, spec):
        return 1
    
    indices = [int(t) for t in re.split(RANGE_SEPARATORS, spec)]
    return indices[1] - indices[0] + 1

if __name__ == "__main__":
    data = sys.stdin.read()
    output = convert(data)
    print(output)
