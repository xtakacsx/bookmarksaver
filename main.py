import os
import pdfkit
import json
from typing import Dict, List, Any
import re


def get_bookmarks() -> Dict:
    with open("bookmarks.json", "r", encoding="utf8") as f:
        file = json.load(f)
        # for child in file["children"][1]["children"]:
        # if child["title"] == "PythonB":
        #     return child
        return file["children"][1]  # toolbar folder


class Folder:
    def __init__(self, path, bookmarks: Dict):
        self.path = os.path.join(path, bookmarks.get("title"))
        self.subfolders = bookmarks.get("children", None)
        self.uri = None
        self.title = None
        if self.subfolders:  # folder has subfolders
            self.foo(self.subfolders)
        if self.subfolders is None:  # no subfolder, this must be a url
            self.title = self.title_clean(self.path.split("\\")[-1])  # file name from the title
            self.path = path  # root folder
        try:
            self.uri = bookmarks["uri"]
        except Exception:
            pass

        # print(self.title)
        # print(self.uri)
        # print(self.path)
        os.makedirs(path, exist_ok=True)
        if self.title is not None:
            file_path = f"{self.path}\\{self.title}.pdf"
            # print(file_path)
            if not os.path.isfile(file_path):
                try:
                    print(f"New file found {file_path}")
                    pdfkit.from_url(url=self.uri, output_path=f"{self.path}\\{self.title}.pdf")
                except Exception as e:
                    print(f"Failed to create {self.title}\n{e}")

    @staticmethod
    def title_clean(title: str) -> str:
        sre = re.sub(r'[\\/:*"<>|.%$^&£]', '', title)  # illegal folder char.
        return sre

    def foo(self, child: List[Dict]) -> None:
        self.subfolders = [Folder(self.path, sub) for sub in child]


fldr = get_bookmarks()
bmf = Folder(os.getcwd(), bookmarks=fldr)
