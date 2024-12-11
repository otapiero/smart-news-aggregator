from typing import Dict, List


class NewsApiConfig:
    """Class to store and manage mappings for countries, categories, and languages.
    made to match the newsapi.ai API."""

    COUNTRY_MAP = {
        "us": "http://en.wikipedia.org/wiki/United_States",
        "israel": "http://en.wikipedia.org/wiki/Israel",
        "uk": "http://en.wikipedia.org/wiki/United_Kingdom",
        "france": "http://en.wikipedia.org/wiki/France",
    }

    CATEGORY_MAP = {
        "politics": "news/Politics",
        "business": "news/Business",
        "technology": "news/Technology",
        "health": "news/Health",
        "sports": "news/Sports",
        "environment": "news/Environment",
        "science": "news/Science",
        "arts_and_entertainment": "news/Arts_and_Entertainment",
    }

    LANGUAGE_MAP = {
        "english": "eng",
        "hebrew": "heb",
        "french": "fra",
    }

    @classmethod
    def get_country_uri(cls, country: str) -> str:
        """Get the URI for the given country."""
        return cls.COUNTRY_MAP.get(country.lower())

    @classmethod
    def get_category_uri(cls, category: str) -> str:
        """Get the URI for the given category."""
        return cls.CATEGORY_MAP.get(category.lower())

    @classmethod
    def get_language_code(cls, language: str) -> str:
        """Get the language code for the given language."""
        return cls.LANGUAGE_MAP.get(language.lower())

    @classmethod
    def get_available_options(cls) -> Dict[str, List[str]]:
        """Get all available options for countries, categories, and languages."""
        return {
            "countries": list(cls.COUNTRY_MAP.keys()),
            "categories": list(cls.CATEGORY_MAP.keys()),
            "languages": list(cls.LANGUAGE_MAP.keys()),
        }
