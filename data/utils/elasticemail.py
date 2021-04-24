import http.client
import urllib.error
import urllib.parse
import urllib.request

USERNAME = "admin@email.test"
API_KEY = "APIKEY"
API_SERVER = "api.elasticemail.com"
API_URI = "/mailer/send"


def send_email(
    to_addr="",
    subject="",
    body_text="",
    body_html="",
    from_addr="",
    from_name="",
    reply_to_email=None,
    reply_to_name=None,
    channel=None,
    attachments=None,
):

    msg_info = {
        "username": USERNAME,
        "api_key": API_KEY,
        "from": from_addr,
        "from_name": from_name,
        "to": to_addr,
        "subject": subject,
        "body_text": body_text,
        "body_html": body_html,
        "reply_to": reply_to_email,
        "reply_to_name": reply_to_name,
        "channel": channel,
        "isTransactional": "true",
    }

    if attachments:
        if type(attachments) == str:
            msg_info["attachments"] = attachments

    params = urllib.parse.urlencode(msg_info)
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain",
    }

    try:
        conn = http.client.HTTPSConnection(API_SERVER)
        conn.request("POST", API_URI, params, headers)
        response = conn.getresponse()

        ret = response.read()
        conn.close()
    except Exception as e:
        ret = str(e)

    return ret
