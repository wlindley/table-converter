
import re


def convert(input: str) -> str:
    output_lines = []
    output_lines.extend(["", "---"])

    for line in input.split("\n"):
        if _is_markdown(line):
            line = _markdown_to_plain(line)

        if _is_header(line):
            continue

        columns = line.split(maxsplit=1)
        for i in range(_extract_range(columns[0])):
            output_lines.append(columns[1])
    
    output_lines.extend(["", "---"])

    return "\n".join(output_lines)

def _is_markdown(line: str) -> bool:
    return line.startswith("|")

def _markdown_to_plain(line: str) -> str:
    return line[1:-1].replace("|", " ")

def _is_header(line: str) -> bool:
    return not re.search("^\d", line)

def _extract_range(spec: str) -> int:
    if "-" not in spec:
        return 1
    
    indices = [int(t) for t in spec.split("-")]
    return indices[1] - indices[0] + 1
