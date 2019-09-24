#!/usr/bin/python3

from google.cloud import language
from google.cloud.language import enums


class LanguageAnalyer(object):
    """LanguageSentimentAnalyser"""

    def __init__(self, lang="zh-Hant", doc_type="plain"):
        """Object that will analyze the content of the strings list provided.

        Args:
            lang (str): Language to use in the analyzer. Defaults to zh-Hant,
                Chinese (Traditional). For other options to provide, reference:
                https://cloud.google.com/natural-language/docs/languages
            doc_type (str): Defines the type of document to analyze.
        """
        self.client = language.LanguageServiceClient()
        self.lang = lang
        self.encode_type = enums.EncodingType.UTF8

        if doc_type == "html":
            self.content_type = enums.Document.Type.HTML
        self.content_type = enums.Document.Type.PLAIN_TEXT

    def analyze(self, string):
        """ Get analysis for string provided.

        Args: string (str): String to analyze.
        """
        # Setup document
        document = {
            "content": string,
            "type": self.content_type,
            "language": self.lang,
        }

        return self.client.analyze_sentiment(
            document, encoding_type=self.encode_type)


def main():
    tweet = LanguageAnalyer(lang="en")
    tweet.analyze("I am very happy today!")


if __name__ == '__main__':
    main()
