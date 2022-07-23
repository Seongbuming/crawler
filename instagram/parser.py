from dataclasses import dataclass
import json
import base64
import argparse
from urllib import parse

@dataclass
class InstagramContent:
    content_url: str
    image_url: str
    author: str
    comments: dict

class InstagramHarParser:
    def __init__(self, har_file, keyword):
        with open(har_file, "r") as file:
            data = json.loads(file.read())
        self.data = data['log']
        self.keyword = keyword
    
    def parse_contents(self):
        prefixes = (
            "https://i.instagram.com/api/v1/tags/web_info/",
            f"https://i.instagram.com/api/v1/tags/{parse.quote(self.keyword)}/sections/",
        )
        contents = [
            json.loads(base64.b64decode(entry['response']['content']['text']).decode("utf-8"))
            for entry
            in self.data['entries']
            if entry['request']['method'] in ["GET", "POST"]
                and entry['request']['url'].startswith(prefixes)
                and 'text' in entry['response']['content'].keys()
        ]
        return contents

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--har_file",
        type=str,
        default="./data/www.instagram.com.har",
        help="The path of .har file containing the network log of the page to parse.",
    )
    arg_parser.add_argument(
        "--keyword",
        type=str,
        required=True,
        help="Search keyword for which to collect data.",
    )

    args = arg_parser.parse_args()

    parser = InstagramHarParser(args.har_file, args.keyword)
    print(len(parser.parse_contents()))
