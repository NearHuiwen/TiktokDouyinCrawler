# -*- coding: utf-8 -*-
# @Author : lihuiwen
# @file : tiktok_crawler
# @Email : huiwennear@163.com
# @Time : 2024/5/23 16:59

"""
    Tiktok评论爬取
"""
from utils.common_utils import CommonUtils

import requests
from urllib.parse import urlparse

class TiktokComment:

    def __init__(self):
        self.common_utils = CommonUtils()
        self.comment_list_headers = {
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': self.common_utils.user_agent,
            'sec-ch-ua-platform': '"Windows"',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

    def get_comment_list(self, req_url):
        aweme_id = urlparse(req_url).path.split("/")[-1]
        ms_token = self.common_utils.get_ms_token()
        req_url = f"https://www.tiktok.com/api/comment/list/?WebIdLastTime=1715249710&aid=1988&app_language=ja-JP&app_name=tiktok_web&aweme_id={aweme_id}&browser_language=zh-CN&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F123.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&count=20&current_region=JP&cursor=0&device_id=7366941338308609569&device_platform=web_pc&enter_from=tiktok_web&focus_state=true&fromWeb=1&from_page=video&history_len=2&is_fullscreen=false&is_non_personalized=false&is_page_visible=true&odinId=7367172442253296673&os=windows&priority_region=&referer=&region=GB&screen_height=1080&screen_width=1920&tz_name=Asia%2FShanghai&webcast_language=zh-Hans&msToken={ms_token}"
        xbogus = self.common_utils.get_xbogus(req_url, self.common_utils.user_agent)
        req_url = req_url + f'&X-Bogus={xbogus}&_signature=_02B4Z6wo000016M20awAAIDAnp.LMKuZmC-jNtUAAI6L17'
        response = requests.request("GET", req_url, headers=self.comment_list_headers,verify=False, timeout=3)
        if (response.text):
            req_json = response.json()
            total = req_json.get('total')
            comments = req_json.get('comments')
            if (comments):
                for comment_index in range(len(comments)):
                    comment_item = comments[comment_index]
                    print(f"爬取成功：{comment_item.get('user').get('nickname')}：{comment_item.get('text')}")
            else:
                print(f"爬取结束：评论数={total}")
        else:
            print(f"爬取失败或没有评论")


if __name__ == '__main__':
    req_url = "https://www.tiktok.com/@.jisvnq/video/7341777664224677153"
    tiktok_comment = TiktokComment()
    tiktok_comment.get_comment_list(req_url)