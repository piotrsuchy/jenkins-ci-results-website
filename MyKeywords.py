# MyKeywords.py
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from datetime import datetime


class MyKeywords:

    @keyword("Log Keyword Execution Time")
    def log_keyword_execution_time(self, keyword_name, *args):
        start_time = datetime.now()
        print(f"Starting keyword: {keyword_name} at {start_time}")
        result = BuiltIn().run_keyword(keyword_name, *args)
        end_time = datetime.now()
        print(f"Ending keyword: {keyword_name} at {end_time}")
        duration = end_time - start_time
        print(f"Keyword execution time: {duration}")
        return result
