import os

from slack_bolt import App

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))


@app.message("knock2")
def ask_who(message, say):
    print("kxx")
    try:
        say(f"Hey there <@{message['user']}>!")
    except Exception as e:
        say(f"Error publishing home tab: {e}")


@app.message("knock")
def ask_who_knocked(client, message):
    channel_id = message["channel"]
    client.chat_scheduleMessage(channel=channel_id, post_at=1601510399, text="Go")

@app.event("app_home_opened")
def update_home_tab(client, event, say):
    say("Hello, I'm Tasuke.")
