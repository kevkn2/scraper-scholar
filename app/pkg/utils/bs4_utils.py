from typing import Optional

from bs4 import Tag


def clean_text(text: str) -> str:
    """Clean and normalize text"""
    if not text:
        return ""
    # Remove extra whitespace and newlines
    text = " ".join(text.split())
    return text.strip()


def extract_text(tag: Optional[Tag]) -> str:
    """Extract and clean text from a tag"""
    return clean_text(tag.get_text()) if tag else ""


def extract_link(tag: Optional[Tag], attr: str = "href") -> str:
    """Extract and clean link/attribute from a tag"""
    return tag.get(attr, "") if tag else ""


def find_div(parent: Tag, class_name: str) -> Optional[Tag]:
    """Find a div by class name"""
    return parent.find("div", class_=class_name) if parent else None
