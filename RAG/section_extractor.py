import re


def extract_sections(document):
    """
    Extract the 30 actual legal sections from the document.
    """

    # Find actual Section 1, not the Contents entry
    start_pattern = (
        r"(?m)^\s*1\.\s*"
        r"Short title,\s*extent and commencement"
        r".*?—\s*\(1\)"
    )

    start_match = re.search(start_pattern, document)

    if not start_match:
        raise ValueError("Actual Section 1 not found.")

    document = document[start_match.start():]

    # Find section numbers
    pattern = r"(?m)^\s*(\d{1,2})\.\s+"

    matches = list(re.finditer(pattern, document))

    sections = []

    for i, match in enumerate(matches):

        section_number = int(match.group(1))

        # Ignore omitted Section 31
        if section_number == 31:
            continue

        start = match.start()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(document)

        section_text = document[start:end].strip()

        first_line = section_text.split("\n")[0].strip()

        title = re.sub(
            rf"^\s*{section_number}\.\s*",
            "",
            first_line
        )

        title = re.split(
            r"\s*[.—-]\s*",
            title,
            maxsplit=1
        )[0].strip()

        sections.append({
            "section": section_number,
            "title": title,
            "text": section_text
        })

    return sections


def add_page_metadata(sections, cleaned_pages):
    """
    Add the page where each section starts.
    """

    # Combine pages but keep track of where each page starts
    document = "\n\n".join(cleaned_pages)

    for section in sections:

        # Find this section's text in the combined document
        position = document.find(section["text"])

        if position == -1:
            section["page"] = None
            continue

        # Determine page from character position
        current_position = 0
        page_number = None

        for i, page in enumerate(cleaned_pages, start=1):

            page_start = current_position
            page_end = current_position + len(page)

            if page_start <= position <= page_end:
                page_number = i
                break

            current_position = page_end + 2  # "\n\n"

        section["page"] = page_number

    return sections