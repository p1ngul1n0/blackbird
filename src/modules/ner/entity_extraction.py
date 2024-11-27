import spacy
from bs4 import BeautifulSoup
from bs4 import MarkupResemblesLocatorWarning
import warnings
import sys
import traceback
import re
from ..utils.parse import download_image

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)


def inialize_nlp_model(config):
    try:
        config.nlp = spacy.load("en_blackbird_osint_ner")
        config.console.print("✔️  Successfully loaded AI model (en_blackbird_osint_ner)")
    except Exception as e:
        config.console.print(f"❌ Could not load AI model (en_blackbird_osint_ner)")
        config.console.print(
            "Please install the model with `pip install en_blackbird_osint_ner`"
        )
        sys.exit()


def extract_meta_tags(html_content):
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        meta_tags = soup.find_all("meta")
        meta_contents = []

        for tag in meta_tags:
            if tag.get("content") and (tag.get("name") or tag.get("property")):
                content = tag["content"]
                name = tag.get("name") if tag.get("name") else tag.get("property")
                new_item = f"{name} - {content}"
                meta_contents.append(new_item)
        return meta_contents
    except Exception as e:
        return []


def extract_json_string(json_content):
    key_value_array = []

    def process_dict(data):
        for key, value in data.items():
            if isinstance(value, dict):
                pass
            elif isinstance(value, str) and value is not None and value != "":
                key_value_array.append(f"{key} - {value}")

    process_dict(json_content)
    return key_value_array


def extract_data_with_ai(config, site, html_content=None, json_content=None):
    avatar_regex = r"(https?://[^\s]+(?:avatar|profile|user)[^\s]*(?:\.jpg|\.jpeg|\.png|\.gif|\.webp|\.svg|\.bmp))"
    extractedMetadata = []
    raw_data = []
    try:
        if html_content:
            metadata_data = extract_meta_tags(html_content)
            raw_data.extend(metadata_data)
        if json_content:
            json_data = extract_json_string(json_content)
            raw_data.extend(json_data)
        for text in raw_data:
            doc = config.nlp(text)
            if len(doc.ents) > 0:
                for d in doc.ents:
                    metadata_item = {
                        "path": None,
                        "name": None,
                        "value": None,
                        "type": None,
                        "downloaded": False,
                        "schema": "JSON" if json_content else "HTML",
                    }
                    metadata_item["name"] = d.label_.capitalize()
                    metadata_item["value"] = d.text

                    if metadata_item["name"] == "Avatar":
                        if not re.match(avatar_regex, d.text):
                            continue
                        metadata_item["type"] = "Image"

                        if config.pdf:
                            metadata_item = download_image(
                                metadata_item, site["name"], config
                            )

                    if metadata_item["name"] == "Name":
                        metadata_item["type"] = "String"

                    if not any(
                        item["name"] == d.label_.capitalize()
                        for item in extractedMetadata
                    ):
                        config.console.print(
                            f"      :right_arrow:  {metadata_item['name']}: {metadata_item['value']} (🤖)"
                        )
                        extractedMetadata.append(metadata_item)
        return extractedMetadata
    except Exception as e:
        config.console.print("❌ Could not extract data with AI")
        config.console.print(e)
        traceback.print_exc()
