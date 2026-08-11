import re


def clean_text(text):
    """
    Clean extracted PDF text.

    Args:
        text (str): Raw page text.

    Returns:
        str: Cleaned text.
    """

    # Remove page markers
    text = re.sub(r"Page \d+ of \d+", "", text)

    # Remove excessive spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Fix escaped section numbers
    text = text.replace(r"\.", ".")

    # Remove common amendment/footnote markers
    text = re.sub(
        r"\d+\s*Subs\..*?(?=\n|$)",
        "",
        text
    )

    # Remove excessive blank lines
    text = re.sub(
        r"\n\s*\n+",
        "\n\n",
        text
    )

    return text.strip()


def clean_pages(pages):
    """
    Clean all PDF pages.

    Args:
        pages (list): Raw page texts.

    Returns:
        list: Cleaned page texts.
    """

    cleaned_pages = []

    for page in pages:
        cleaned_pages.append(clean_text(page))

    return cleaned_pages