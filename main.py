import configparser, re
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from database import *
from helper import remove_emojis, url_regex


# +------------------user credentials-------------------+
config = configparser.ConfigParser()
config.read("config.ini")
api_id = config["user"]["api_id"]
api_hash = config["user"]["api_hash"]
phone_number = config["user"]["phone_number"]
device_model = config["user"]["device_model"]
bot_admin = config["user"]["admin"]
archive_chanenl = config["user"]["archive_channel"]

data_base_name = config["db"]["data_base_name"]
blacklist_table_name = config["db"]["blacklist_table_name"]
links_table_name = config["db"]["links_table_name"]
blacklist_file = config["db"]["blacklist_file"]
# +-------------------------------------------------------+


print("started")

# +----------------------database--------------------------+
conn = create_connection(data_base_name)
if conn is not None:
    create_blacklist_table(conn=conn, table_name=blacklist_table_name)
    setup_data(
        conn=conn, table_name=blacklist_table_name, blacklist_file=blacklist_file
    )
    create_links_table(conn=conn, table_name=links_table_name)
c = conn.cursor()


# +--------------------------------------------------------+


app = Client(
    "AntiBet",
    api_id=api_id,
    api_hash=api_hash,
    phone_number=phone_number,
    app_version="1.0",
    device_model=device_model,
)

# Admin help
@app.on_message(
    filters=filters.user(users=bot_admin) & filters.command(["help"], prefixes="!")
)
async def command(client, message):
    txt = """
    ⭕️**help**
    🔰**__join :__**  `!join|link or id`
    example:
    `!join|https://t.me/joinchat/VRSmq`
    `!join|webamoozir`
    `+-------------------------------+`
    🔰**__leave :__**  `!leave|link or id`
    example:
    `!leave|https://t.me/joinchat/VRSmq`
    `!leave|webamoozir`
    `+-------------------------------+`
    🔰**__add to blacklist :__**  `!addword|word`
    example:
    `!addword|bet`
    `!addword|gamble`
    `+-------------------------------+`
    🔰**__show blacklist :__**  `!blacklist`
    example:
    `!blacklist`
    `+-------------------------------+`
    🔰**__remove from blacklist :__**  `!rmword|word`
    example:
    `!rmword|bet`
    `!rmword|gamble`
    `+-------------------------------+`
    🔰**__show Links :__**  `!links`
    example:
    `!links`
    `+-------------------------------+`

    
    
    """
    await message.reply(txt, parse_mode="markdown")


# manual join
@app.on_message(filters=filters.user(users=bot_admin) & filters.regex("^!join\|"))
async def join_admin(client, message):
    raw_text = message.text
    link = raw_text.split("|")[1]
    try:
        await client.join_chat(link)
        await message.reply_text("I'm joining the link")
    except UserAlreadyParticipant:
        await message.reply_text("I'm already participant in this link ")
    except Exception as e:
        await message.reply_text(e)


# manual leave
@app.on_message(filters=filters.user(users=bot_admin) & filters.regex("^!leave\|"))
async def leave_admin(client, message):
    raw_text = message.text
    link = raw_text.split("|")[1]
    try:
        await client.leave_chat(link)
        await message.reply_text("I'm leaving the chat")
    except Exception as e:
        await message.reply_text(e)


# add to blacklist
@app.on_message(filters=filters.user(users=bot_admin) & filters.regex("^!addword\|"))
async def add_to_blacklist(client, message):
    raw_text = message.text
    word = raw_text.split("|")[1]
    try:
        add_to_blacklist_db(conn=conn, table_name=blacklist_table_name, word=word)
        await message.reply_text(" added sucessfully")
    except Exception as e:
        await message.reply_text(f"an error accourd :{e}")


# remove from blacklist
@app.on_message(filters=filters.user(users=bot_admin) & filters.regex("^!rmword\|"))
async def remove_from_blacklist(client, message):
    raw_text = message.text
    word = raw_text.split("|")[1]
    try:
        remove_from_blacklist_db(conn=conn, table_name=blacklist_table_name, word=word)
        await message.reply_text(" removed sucessfully")
    except Exception as e:
        await message.reply_text(f"an error accourd :{e}")


# show all words in blacklist
@app.on_message(filters=filters.user(users=bot_admin) & filters.regex("^!blacklist"))
async def show_all_words(client, message):
    try:
        words = show_all_words_db(conn=conn, table_name=blacklist_table_name)
        await message.reply_text(words)
    except Exception as e:
        await message.reply_text(f"an error accourd :{e}")


# show all gatherd links
@app.on_message(filters=filters.user(users=bot_admin) & filters.regex("^!links"))
async def show_all_links(client, message):
    try:
        links = show_all_links_db(conn=conn, table_name=links_table_name)
        await message.reply_text(links, disable_web_page_preview=True)
    except Exception as e:
        await message.reply_text(f"an error accourd :{e}")


# link finder
@app.on_message(filters=~filters.private & filters.regex(url_regex))
async def link_finder(client, message):

    raw_text = (
        remove_emojis(message.text if message.text != None else message.caption)
        .replace("#", " ")
        .replace("_", " ")
    )

    for word in raw_text.split(" "):
        if is_present(conn=conn, table_name=blacklist_table_name, word=word):
            links = re.findall(url_regex, raw_text)
            channel_username = message.chat.username
            try:
                await message.forward(archive_chanenl)
            except:
                pass
            for link in links:
                c.execute(
                    f"""INSERT OR IGNORE INTO {links_table_name} (channel_username,link) VALUES(?,?);""",
                    (channel_username, link),
                )
            conn.commit()
            break


@app.on_message(filters=~filters.private)
async def link_finder_2(client, message):
    links = []
    if message.entities != None:
        links = [item.url for item in message.entities if item.url != None]

    if message.caption_entities != None:
        links = [item.url for item in message.caption_entities if item.url != None]

    channel_username = message.chat.username
    if links != []:
        raw_text = (
            remove_emojis(message.text if message.text != None else message.caption)
            .replace("#", " ")
            .replace("_", " ")
        )
        for word in raw_text.split(" "):
            if is_present(conn=conn, table_name=blacklist_table_name, word=word):
                try:
                    await message.forward(archive_chanenl)
                except:
                    pass
                for link in links:
                    c.execute(
                        f"""INSERT OR IGNORE INTO {links_table_name} (channel_username,link) VALUES(?,?);""",
                        (channel_username, link),
                    )
                conn.commit()
                break


app.run()
