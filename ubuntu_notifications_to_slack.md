## Send your Ubuntu notifications to your Slack

Recently I stumbled upon a situation where for some unavoidable circumstances I could only login to a platform from my desktop and whenever a notification is received from that platform I needed the notification to be on my phone 🤷🏽‍♂️

Since I'm using Ubuntu 20.x I crafted this horrible script in a rush that taps into the `FreeDesktop notification D-Bus protocol` and sends a Slack notification to my phone via Slack webhook. Notifications from Chrome, Discord, etc are sent via that protocol so you can interact with any notification that you can directly view from Ubuntu's notification panel. 

[ubuntu_to_slack.py](scripts/ubuntu_to_slack.py)

I don't know much about D-Bus protocol and it might be poorly coded but it's getting the job done atm 🤝.

I redacted some of the things from the original script but basically, the notification contents will be inside the `args_list` extracted via `get_args_list()` from the `message` object. 

If you are trying to intercept a particular notification for example a push notification from a website via Google Chrome, check the values in the argument list and adjust your script like that.

Built and shared for educational purposes, I bear no liability if anything bad happens (for example your computer blows up 💥) due to the usage of this script.