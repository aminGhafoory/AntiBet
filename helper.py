import re


telegram_handle_regex = re.compile("(?:^|[^@\w])@(?:\w{5,32})\b")  # @blah


telegram_link_regex = re.compile(
    r"(?:https?:)?\/\/(?:t(?:elegram)?\.me)\/joinchat\/(?:[a-zA-Z0-9_-]{16})"
)  # https://t.me/joinchat/blah


telegram_link_regex2 = re.compile(
    r"(?:https?:)?\/\/(?:t(?:elegram)?\.me)\/(?!joinchat)(?!proxy)(?:[a-zA-Z0-9_]{5,32})"
)  # https://t.me/blah


telegram_link_regex3 = re.compile(
    r"(?:https?:)?\/\/(?:t(?:elegram)?\.me)\/\+(?:[A-Za-z0-9-_]{16})"
)  # https://t.me/+blah


telegram_link_regex4 = re.compile(r"t.me\/(?!joinchat)(?!proxy\?)[a-zA_Z0-9_]{5,32}")


url_regex = re.compile(
    r"http[s]?://(?!t(?:elegram)?\.me)(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
)


def remove_emojis(data):
    emoj = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        "]+",
        re.UNICODE,
    )
    return re.sub(emoj, " ", data)
