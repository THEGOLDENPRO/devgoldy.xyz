import logging
from pathlib import Path
from pyromark import Markdown

__all__ = ()

logger = logging.getLogger(__name__)

class MarkdownSections():
    def __init__(self, basic_markdown: Markdown):
        self.__basic_markdown = basic_markdown

        self.__parsed_markdown_sections: dict[str, str] = self.__parse_all_markdown()

    def get_section_html(self, section_id: str) -> str:
        return self.__parsed_markdown_sections[section_id]

    # might reuse this function somewhere
    def __parse_all_markdown(self):
        logger.debug("Parsing all markdown files...")

        markdown_folder_path = Path("./markdown")

        parsed_markdown_sections: dict[str, str] = {}

        for markdown_path in markdown_folder_path.glob("*.md"):
            logger.debug(f"Opening and parsing '{markdown_path.name}' markdown...")

            with markdown_path.open("r") as file:
                parsed_markdown = self.__basic_markdown.html(file.read())

            parsed_markdown_sections[markdown_path.stem] = parsed_markdown

        return parsed_markdown_sections