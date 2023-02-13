import json
import pandas as pd
import traceback
import requests
import re
import datetime
from typing import Tuple
from bs4 import BeautifulSoup
#from .dto import *

class GooglePlayReviewParser:
    def __init__(self, app_id: str):
        self.app_id = app_id
        self.cookies = None
        self.headers = {
            "accept-encoding": "gzip, deflate, br",
        }
    
    def run(self, output_file: str = "") -> list:
        contents, scripts = self.request_app_details()
        review_ds_keys = self.find_review_ds_keys(contents)
        review_data = self.crawl_review_data(scripts, review_ds_keys)
        
        if output_file is not None and len(output_file) > 0:
            if output_file[-4:].lower() == ".csv":
                # Save as csv
                df = pd.DataFrame(review_data)
                df.to_csv(output_file)
            elif output_file[-5:].lower() == ".json":
                # Save as json
                with open(output_file, "w") as file:
                    string = json.dumps(review_data)
                    file.write(string)
            else:
                # Save as text
                with open(output_file, "w", encoding="UTF-8") as file:
                    string = str(review_data)
                    file.write(string)
            print(f"Data saved in `{output_file}`.")
        
        return review_data

    def request_app_details(self) -> Tuple[str, list]:
        response = requests.get(
            url="https://play.google.com/store/apps/details",
            params={
                "id": self.app_id,
                "hl": "ko",
            },
            headers=self.headers,
            cookies=self.cookies,
        )
        
        try:
            app_details = response.text
            scripts = BeautifulSoup(response.text, "html.parser").select("script")
        except Exception:
            print(response.status_code, response.content)
            raise Exception("Failed to load `app_details`.")
        
        return app_details, scripts

    def find_review_ds_keys(self, contents: str) -> list:
        # Find data service keys
        services_regex = r"var AF_dataServiceRequests = ([^;]*)"
        services_match = re.findall(services_regex, contents, re.MULTILINE)
        services = services_match[0]
        review_ds_key_regex = r"\'(ds:[0-9]+)\' : {id:\'oCPfdb\'"
        review_ds_keys = re.findall(review_ds_key_regex, services, re.MULTILINE)

        return review_ds_keys
    
    def parse_review(self, review_row: list):
        writed_time = datetime.datetime.utcfromtimestamp(review_row[5][0])
        writed_time = writed_time.strftime("%Y-%m-%d %H:%M")

        return {
            "review_id": review_row[0],
            "author": review_row[1][0],
            "review_text": review_row[4],
            "rating": review_row[2],
            "writed_time": writed_time,
        }
    
    def crawl_review_data(self, scripts: list, review_ds_keys: list) -> list:
        review_data, next_page = self.review_first_page(scripts, review_ds_keys)

        while len(next_page) > 0:
            review_data_partial, next_page = self.review_other_page(next_page)
            review_data += review_data_partial

        return review_data
    
    def review_first_page(self, scripts: list, review_ds_keys: list) -> Tuple[list, str]:
        review_data = []
        next_page = ""

        for script in scripts:
            ds_key_regex = r"AF_initDataCallback\({key: \'(ds:\d+)\',"
            ds_keys = re.findall(ds_key_regex, script.text, re.MULTILINE)
            if len(ds_keys) > 0 and ds_keys[0] in review_ds_keys:
                review_data_regex = r"data:([\[].*[\]]), sideChannel: {}}\);$"
                review_data_str = re.findall(review_data_regex, script.text, re.MULTILINE)[0]
                review_data_raw = json.loads(review_data_str)
                
                review_data = list(map(self.parse_review, review_data_raw[0]))
                next_page = str(review_data_raw[1][1])
                break
        
        return review_data, next_page

    def review_other_page(self, page_hash: str) -> Tuple[list, str]:
        review_data = []
        next_page = ""

        try:
            f_req_format = '[[["oCPfdb","[null,[2,1,[100,null,\\"%s\\"]],[\\"%s\\",7]]",null,"generic"]]]'
            response = requests.post(
                url="https://play.google.com/_/PlayStoreUi/data/batchexecute",
                params={
                    "rpcids": "oCPfdb",
                    "hl": "ko",
                },
                data={
                    "f.req": f_req_format % (page_hash, self.app_id)
                },
                headers=self.headers,
                cookies=self.cookies,
            )
            review_data_raw = json.loads(json.loads(response.text[6:])[0][2])

            review_data = list(map(self.parse_review, review_data_raw[0]))
            if review_data_raw[1] is None:
                print("Scrapped all reviews.")
            else:
                next_page = review_data_raw[1][1]
        except Exception:
            traceback.print_exc()
            pass

        return review_data, next_page
