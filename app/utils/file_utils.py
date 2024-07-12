import base64
import json
import os
import re
from io import BytesIO

import pdfplumber
from PIL import Image
from strenum import StrEnum

PROJECT_BASE = os.getenv("RAG_PROJECT_BASE") or os.getenv("RAG_DEPLOY_BASE")
RAG_BASE = os.getenv("RAG_BASE")

class FileType(StrEnum):
    PDF = 'pdf'
    VISUAL = 'visual'



def get_project_base_directory(*args):
    global PROJECT_BASE
    if PROJECT_BASE is None:
        PROJECT_BASE = os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                os.pardir,
                os.pardir,
            )
        )

    if args:
        return os.path.join(PROJECT_BASE, *args)
    return PROJECT_BASE




def get_home_cache_dir():
    dir = os.path.join(os.path.expanduser('~'), ".ragflow")
    try:
        os.mkdir(dir)
    except OSError as error:
        pass
    return dir




def filename_type(filename):
    filename = filename.lower()
    if re.match(r".*\.pdf$", filename):
        return FileType.PDF.value

    if re.match(r".*\.(jpg|jpeg|png|tif|gif|pcx|tga|exif|fpx|svg|psd|cdr|pcd|dxf|ufo|eps|ai|raw|WMF|webp|avif|apng|icon|ico|mpg|mpeg|avi|rm|rmvb|mov|wmv|asf|dat|asx|wvx|mpe|mpa|mp4)$", filename):
        return FileType.VISUAL.value

    return FileType.OTHER.value


def thumbnail(filename, blob):
    filename = filename.lower()
    if re.match(r".*\.pdf$", filename):
        pdf = pdfplumber.open(BytesIO(blob))
        buffered = BytesIO()
        pdf.pages[0].to_image(resolution=32).annotated.save(buffered, format="png")
        return "data:image/png;base64," + \
            base64.b64encode(buffered.getvalue()).decode("utf-8")

    if re.match(r".*\.(jpg|jpeg|png|tif|gif|icon|ico|webp)$", filename):
        image = Image.open(BytesIO(blob))
        image.thumbnail((30, 30))
        buffered = BytesIO()
        image.save(buffered, format="png")
        return "data:image/png;base64," + \
            base64.b64encode(buffered.getvalue()).decode("utf-8")



def traversal_files(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            fullname = os.path.join(root, f)
            yield fullname
