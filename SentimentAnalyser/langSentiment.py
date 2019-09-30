#!/usr/bin/python3

import os
import pyodbc

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


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
            document, encoding_type=self.encode_type).document_sentiment


def main():
    tweet = LanguageAnalyer()
    
    # Create connection to database
    server = 'tcp:ec601database-server.database.windows.net, 1433'
    database = 'ec601database'
    username = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWD')

    cnxn = pyodbc.connect('DRIVER={ODBC DRIVER 17 for SQL Server};\
                           SERVER=' + server + ';\
                           DATABASE=' + database + ';\
                           UID=' + username + ';\
                           PWD=' + password)
    cursor = cnxn.cursor()

    # Get the table data
    cursor.execute('select * from test_defaultKeywordsSearchStorage')

    # Update query
    update_q = "UPDATE test_defaultKeywordsSearchStorage SET TweetsNLPScore = ? WHERE TweetsId = ?;"

    # Iterate through rows
    for row in cursor.fetchall():
        # Get sentiment of individual tweet
        sentiment = tweet.analyze(row.TweetsText)
        cursor.execute(update_q, sentiment.score*10, row.TweetsId)
    
    # Commit changes to DB
    cnxn.commit()
    print("Database updated with score!")


if __name__ == '__main__':
    main()
