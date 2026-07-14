import logging
from pathlib import Path
from pyromark import Markdown

__all__ = ()

logger = logging.getLogger(__name__)

class MarkdownSections():
    def __init__(self, basic_markdown: Markdown, debug_mode: bool):
        self.__debug_mode = debug_mode
        self.__basic_markdown = basic_markdown

        self.__parsed_markdown_sections: dict[str, str] = {}

    def get_section_html(self, section_id: str) -> str:
        if self.__parsed_markdown_sections == {} or self.__debug_mode:
            self.__parse_all_markdown()

        return self.__parsed_markdown_sections[section_id]

    def __parse_all_markdown(self) -> None:
        logger.debug("Parsing all markdown files...")

        markdown_folder_path = Path("./markdown")

        for markdown_path in markdown_folder_path.glob("*.md"):
            logger.debug(f"Opening and parsing '{markdown_path.name}' markdown...")

            with markdown_path.open("r") as file:
                parsed_markdown = self.__basic_markdown.html(file.read())

            self.__parsed_markdown_sections[markdown_path.stem] = parsed_markdown