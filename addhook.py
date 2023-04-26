#!/usr/bin/env python3
import requests
import logging
import json
import argparse

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger("addhook")

parser=argparse.ArgumentParser(prog="addhook", description="Add webhook to all repos")
parser.add_argument("-t", "--token", help="GitHub personal token", required=True)
parser.add_argument("-o", "--org", action="append", help="GitHub organization", required=True)
parser.add_argument("-w", "--webhook", help="Webhook to add", default="https://wfnotify.codenotary.io/webhook")
parser.add_argument("-s", "--secret", help="Webhook secret", required=True)
args = parser.parse_args()

def check_hook(repo, token):
	logger.debug("Using token: %s", token)
	logger.debug("Using repo: %s", repo)
	headers={"Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}", "X-GitHub-Api-Version": "2022-11-28"}
	url=f"https://api.github.com/repos/{repo}/hooks"
	r=requests.get(url, headers=headers)
	if r.status_code not in [200,201]:
		logger.error("Unable to fetch repo webhooks")
		logger.error("Error %d. Response: %s",r.status_code, r.text)
		return
	logger.debug("Checking hooks")
	for t in r.json():
		if "config" in t and "url" in t["config"]:
			hookUrl=t["config"]["url"]
			logger.debug(" - %s", t["config"]["url"])
			if hookUrl == args.webhook:
				logger.info("Hook found")
				return
		else:
			logger.debug("- %s", t)

	logger.info("Hook not found, adding")
	reqdata={"name":"web","active":True,"events":["workflow_run"],"config":{"url":args.webhook,"content_type":"json","insecure_ssl":"0", "secret": args.secret}}
	r=requests.post(url, headers=headers, data=json.dumps(reqdata))
	if r.status_code not in [200, 201]:
		logger.info("Hook added for %s", repo)
	else:
		logger.error("Unable to add repo webhooks")
		logger.error("Error %d. Response: %s",r.status_code, r.text)

def get_repos(org, token):
	logger.debug("Fetching repos for %s", org)
	headers={"Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}", "X-GitHub-Api-Version": "2022-11-28"}
	url=f"https://api.github.com/orgs/{org}/repos"
	repos=[]
	n=1
	while True:
		reqdata={"page": n, "per_page": 30}
		r=requests.get(url, headers=headers, params=reqdata)
		if r.status_code not in [200,201]:
			logger.error("Unable to fetch repos")
			logger.error("Error %d. Response: %s",r.status_code, r.text)
			return
		jresp=r.json()
		newrepos=["{}/{}".format(org,x["name"]) for x in jresp]
		repos.extend(newrepos)
		if len(newrepos)!=30:
			break
		n=n+1
	return repos
		
repolist=[]
for o in args.org:
	repolist.extend(get_repos(o, args.token))


for repo in repolist:
	print(repo)
	check_hook(repo, args.token)
