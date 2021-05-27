import os

import logging
import re

logging.basicConfig(level=logging.DEBUG)

from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt import App, Ack

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)


def clean_emoji(emoji):
    return emoji.replace(":", "").replace('"', "").strip()


@app.message("tsk poll")
def ask_who(message, say, client, logger):
    try:
        logger.info(message)

        # Parse message
        outerGroup = re.compile("\((.+)\)")
        pollMsgMatch = outerGroup.search(message["text"])
        pollMsg = pollMsgMatch.group(1)

        msgBody = pollMsg.split(",")

        channel_id = message["channel"]
        response = client.chat_postMessage(
            channel=channel_id,
            text="*{}* _poll created by {}._".format(msgBody[0], message["user"]),
        )

        channel_id = response["channel"]
        ts = response["ts"]

        for i in range(1, len(msgBody)):
            client.reactions_add(
                channel=channel_id, name=clean_emoji(msgBody[i]), timestamp=ts
            )

    except Exception as e:
        logger.error(f"Error: {e}")


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
