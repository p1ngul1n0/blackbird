import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
)

from ..utils.http_client import do_sync_request
from ..utils.log import logError
from ..utils.parse import extractMetadata
from json import dumps
from urllib.parse import urlencode

metadataParams = [
    {"schema": "JSON", "type": "String", "name": "User ID", "path": ["user", "pk_id"]},
    {
        "schema": "JSON",
        "type": "String",
        "name": "Full Name",
        "path": ["user", "full_name"],
    },
    {
        "schema": "JSON",
        "type": "String",
        "name": "Biography",
        "path": ["user", "biography"],
    },
    {
        "schema": "JSON",
        "type": "String",
        "name": "Follower Count",
        "path": ["user", "follower_count"],
    },
    {
        "schema": "JSON",
        "type": "String",
        "name": "Following Count",
        "path": ["user", "following_count"],
    },
    {
        "schema": "JSON",
        "type": "String",
        "name": "External URL",
        "path": ["user", "external_url"],
    },
    {
        "schema": "JSON",
        "type": "String",
        "name": "Category",
        "path": ["user", "category"],
    },
    {
        "schema": "JSON",
        "type": "String",
        "name": "Is Verified",
        "path": ["user", "is_verified"],
    },
]

metadataParams2 = [
    {"schema": "JSON", "type": "String", "name": "Email Sent", "path": ["email_sent"]},
    {"schema": "JSON", "type": "String", "name": "SMS Sent", "path": ["sms_sent"]},
    {"schema": "JSON", "type": "String", "name": "WhatsApp Sent", "path": ["wa_sent"]},
    {
        "schema": "JSON",
        "type": "String",
        "name": "Obfuscated Email",
        "path": ["obfuscated_email"],
    },
    {
        "schema": "JSON",
        "type": "String",
        "name": "Obfuscated Phone",
        "path": ["obfuscated_phone"],
    },
    {
        "schema": "JSON",
        "type": "String",
        "name": "Is Private",
        "path": ["user", "is_private"],
    },
    {
        "schema": "JSON",
        "type": "String",
        "name": "Has Valid Phone",
        "path": ["has_valid_phone"],
    },
    {
        "schema": "JSON",
        "type": "String",
        "name": "Can Email Reset",
        "path": ["can_email_reset"],
    },
    {
        "schema": "JSON",
        "type": "String",
        "name": "Can SMS Reset",
        "path": ["can_sms_reset"],
    },
    {
        "schema": "JSON",
        "type": "String",
        "name": "Can WhatsApp Reset",
        "path": ["can_wa_reset"],
    },
    {
        "schema": "JSON",
        "type": "String",
        "name": "Facebook Login Option",
        "path": ["fb_login_option"],
    },
    {"schema": "JSON", "type": "String", "name": "Status", "path": ["status"]},
]


def get_user_id(username, session_id, config):
    try:
        headers = {"User-Agent": "iphone_ua", "x-ig-app-id": "936619743392459"}
        cookies = {"sessionid": session_id}
        response = do_sync_request(
            method="GET",
            url=f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
            config=config,
            data=None,
            customHeaders=headers,
            cookies=cookies,
        )
        user_id = response.json()["data"]["user"]["id"]
        if config.verbose:
            config.console.print(f"[Instagram] Acquired {username} user ID")
        return user_id

    except Exception as e:
        logError(e, f"[Instagram] Coudn't acquire {username} user ID", config)
        return False


def get_instagram_account_info(username, session_id, config):
    extractedMetadata = []
    try:
        user_id = get_user_id(username, session_id, config)

        if user_id:
            url = f"https://i.instagram.com/api/v1/users/{user_id}/info/"
            response = do_sync_request(
                method="GET",
                url=url,
                config=config,
                data=None,
                customHeaders={"User-Agent": "Instagram 55.0.0.00.0"},
                cookies={"sessionid": session_id},
            )
            data = response.json()
            response = {"json": data}

            if data:
                metadata = extractMetadata(
                    metadataParams, response, "Instagram", config
                )
                extractedMetadata.extend(metadata)

                json_data = dumps(
                    {"q": username, "skip_recovery": "1"}, separators=(",", ":")
                )
                data = urlencode({"signed_body": f"SIGNATURE.{json_data}"})

                headers = {
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "X-IG-App-ID": "124024574287414",
                    "User-Agent": "Instagram 103.0.0.0.1",
                }

                response = do_sync_request(
                    method="POST",
                    url="https://i.instagram.com/api/v1/users/lookup/",
                    config=config,
                    data=data,
                    customHeaders=headers,
                )
                data = response.json()
                response = {"json": data}

                if data:
                    metadata = extractMetadata(
                        metadataParams2, response, "Instagram", config
                    )
                    extractedMetadata.extend(metadata)

                return extractedMetadata
    except Exception as e:
        logError(e, f"[Instagram] Coudn't acquire more metadata", config)
        return False
