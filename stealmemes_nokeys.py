#!/bin/python3
import json
import requests
from os import path


# Parameters for Discord
AUTHORIZATION = '[DISCORD AUTHORIZATION PARAMETER]'
COOKIE = '[DISCORD COOKIES]'
CHANNEL = '[INSERT CHANNEL]' 


# Download function to download content
# url: URL to download from  
# filename: Name for file to save
# cookie: Discord cookies
# authorization: Discord auth
def download(url, filename, cookie, authorization):
    r = requests.get(url, params={'limit':'100'}, headers={'authorization': authorization,\
            'cookie': cookie, 'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleW'
            'ebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 Edg/87.0.664.41'},\
            allow_redirects=True)
    if not path.exists('stolen memes/{file}'.format(file=filename)):
        with open('stolen memes/{file}'.format(file=filename), 'wb') as file:
            file.write(r.content)
    else:
        i = 0
        while path.exists('stolen memes/{i}-{file}'.format(i=i, file=filename)):
            i = i + 1
        with open('stolen memes/{i}-{file}'.format(i=i, file=filename), 'wb') as file:
            file.write(r.content)


# Get group of messages on Discord
# channel: Channel ID
# prev_group: Last message id gotten
def get_next_group(channel, prev_group=None):
    if prev_group is None:
        r = requests.get('https://discord.com/api/v8/channels/{channel}/messages'.format(channel=channel),\
                params={'limit':'100'}, headers={'authorization': AUTHORIZATION, 'cookie': COOKIE,\
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 Edg/87.0.664.41'})
    else:
        r = requests.get('https://discord.com/api/v8/channels/{channel}/messages'.format(channel=channel),\
                params={'limit':'100', 'before':prev_group}, headers={'authorization': AUTHORIZATION,\
                'cookie': COOKIE, 'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 Edg/87.0.664.41'})
    
    attachment_sets = [msg['attachments'] for msg in json.loads(r.text)]

    for attachment_set in attachment_sets:
        for attachment in attachment_set:
            print("[*] Downloading {filename} from {url}...".format(filename=attachment['filename'], url=attachment['proxy_url']))
            download(attachment['proxy_url'], attachment['filename'], COOKIE, AUTHORIZATION)

    ld = json.loads(r.text)
    if len(ld) > 0:
        prev_group = json.loads(r.text)[-1]['id']
        return prev_group
    else:
        return None


# Main
if __name__ == "__main__":
    prev = get_next_group(CHANNEL)
    while prev is not None:
        prev = get_next_group(CHANNEL, prev)
