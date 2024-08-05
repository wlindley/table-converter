
from pathlib import Path
import re
import sys
from typing import List

RANGE_SEPARATORS = "[-–—−]"  # hyphen, endash, emdash, minus
RANGE_REGEX = f"(\\d+\\s?{RANGE_SEPARATORS}\\s?\\d+\\s)"
SINGLE_REGEX = "(\\d+\\s)"
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

def convert_single_words(input: str) -> str:
    output_lines = []
    _add_header_footer(output_lines)

    for line in input.split():
        if _is_only_number(line):
            continue
        output_lines.append(line)

    _add_header_footer(output_lines)
    return "\n".join(output_lines)

def _is_only_number(line: str) -> bool:
    return re.search("^\\d+.?$", line)

def copy_encounter_tables(src: str, dst: str) -> None:
    filenames = _get_local_files_containing(src)
    for src_name in filenames:
        dst_name = src_name.replace(src, dst)
        _copy_and_replace_contents(src_name, dst_name, src, dst)

def _get_local_files_containing(src: str) -> List[str]:
    dir = Path(".")
    return [p.name for p in dir.glob(f"*{src}*")]

def _copy_and_replace_contents(src_name: str, dst_name: str, src: str, dst: str) -> None:
    with open(src_name, "r") as src_file:
        with open(dst_name, "w") as dst_file:
            contents = src_file.read()
            contents = contents.replace(src, dst)
            dst_file.write(contents)

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "single":
        data = sys.stdin.read()
        output = convert_single_words(data)
        print(output)
    if len(sys.argv) >= 4 and sys.argv[1] == "encounter":
        copy_encounter_tables(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 1:
        data = sys.stdin.read()
        output = convert(data)
        print(output)
    else:
        print(f"Unknown options for {sys.argv}")
    
