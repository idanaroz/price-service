import uuid
from typing import Dict, List
import re
import requests
from bs4 import BeautifulSoup

from common.database import Database
from models.model import Model


class Item(Model):
    def __init__(self, url: str, tag_name: str, query: Dict, _id: str = None):
        self.url = url
        self.tag_name = tag_name
        self.query = query
        self.price = None
        self.collection = "items"
        self._id = _id or uuid.uuid4().hex

    def __repr__(self):
        return f"<Item {self.url}>"

    def load_price(self) -> float:
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()

        pattern = re.compile(r"(\d+,?\d*\.\d\d)")
        match = pattern.search(string_price)
        found_price = match.group(1)
        without_comma = found_price.replace(",", "")
        self.price = float(without_comma)
        return self.price

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "url": self.url,
            "tag_name": self.tag_name,
            "query": self.query
        }

    def save_to_mongo(self):
        Database.insert(self.collection, self.json())

    @classmethod
    def get_by_id(cls, _id):
        item_json = Database.find_one("items", {"_id": _id})
        return cls(**item_json)

    @classmethod
    def all(cls) -> List:
        items_from_db = Database.find("items", {})
        return [cls(**item) for item in items_from_db]
        # return [Item(_id=item['_id'],
        #              url=item['url'],
        #              query=item['query'] ...  )
        #         for item in items_from_db]
