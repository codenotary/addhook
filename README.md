# addhook
Adds webhook to all repositories from one (or more) organizations

## Usage
```
usage: addhook [-h] -t TOKEN -o ORG [-w WEBHOOK] -s SECRET

Add webhook to all repos

options:
  -h, --help            show this help message and exit
  -t TOKEN, --token TOKEN
                        GitHub personal token
  -o ORG, --org ORG     GitHub organization
  -w WEBHOOK, --webhook WEBHOOK
                        Webhook to add
  -s SECRET, --secret SECRET
                        Webhook secret
```

This script adds a webhook to all repositories it can find in one (or more) organizations. That webhook will only be tied and triggered on `workflow_run` events.

Specify the organization with flag `-o`, that can be used multiple times (e.g.: `-o foo -o bar`).

Use flag `-w` to set the webhook url; use the full url, including the schema (i.e., `http` or `https`).

It is (at the moment) mandatory to specify a secret: use flag `-s` for that.

To access GitHub APIs, the script needs an access token. Get a personal token from github; you need to use "classical" tokens. Remember to allow the token to access (in write mode) webhook settings.