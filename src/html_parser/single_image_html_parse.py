from bs4 import BeautifulSoup, Comment
from bs4.element import NavigableString, Tag
from typing import Optional


def single_image_html_parse(html_content: str) -> Optional[Tag]:
    bs = BeautifulSoup(html_content, "html.parser")

    # Get all contents (elements AND text nodes, excluding comments)
    all_contents = []

    for content in bs.contents:
        if isinstance(content, Comment):
            continue
        elif isinstance(content, NavigableString):
            if content.strip():
                return None  # Nonempty text node -> quit.
        else:
            # Collect all non-text nodes
            all_contents.append(content)

    # Check if there's exactly one element and it's an img tag
    if (
        len(all_contents) == 1
        and hasattr(all_contents[0], "name")
        and all_contents[0].name == "img"
    ):
        return all_contents[0]
    else:
        return None
