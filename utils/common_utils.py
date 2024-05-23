# -*- coding: utf-8 -*-
# @Author : lihuiwen
# @Email : huiwennear@163.com
# @Time : 2024/5/23 16:59
import json
import logging
import os
import re
import time
import urllib

import random

import requests
from py_mini_racer import MiniRacer



class CommonUtils(object):
    def __init__(self):


        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'

        js_path = os.path.dirname(os.path.abspath(__file__))
        self.x_bogus_js_path = os.path.join(js_path, 'x_bogus.js')
        self.a_bogus_js_path = os.path.join(js_path, 'a_bogus.js')

        with open(self.x_bogus_js_path, 'r', encoding='utf-8') as f:
            x_bogus_js_code = f.read()
        self.x_bogus_ctx = MiniRacer()
        self.x_bogus_ctx.eval(x_bogus_js_code)

        with open(self.a_bogus_js_path, 'r', encoding='utf-8') as f:
            a_bogus_js_code = f.read()
        self.a_bogus_ctx = MiniRacer()
        self.a_bogus_ctx.eval(a_bogus_js_code)

        self.ac_sign_js_path = os.path.join(js_path, 'ac_sign.js')

    def get_xbogus(self, req_url, user_agent):
        """
        xbogus加密
        :param req_url:
        :param user_agent:
        :return:
        """
        query = urllib.parse.urlparse(req_url).query
        xbogus = self.x_bogus_ctx.call('sign', query, user_agent)
        return xbogus

    def get_abogus(self, req_url, user_agent):
        """
        xbogus加密
        :param req_url:
        :param user_agent:
        :return:
        """
        query = urllib.parse.urlparse(req_url).query
        abogus = self.a_bogus_ctx.call('generate_a_bogus', query, user_agent)
        return abogus


    def get_ms_token(self, randomlength=107):
        """
        根据传入长度产生随机字符串
        """
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789='
        length = len(base_str) - 1
        for _ in range(randomlength):
            random_str += base_str[random.randint(0, length)]
        return random_str


    def get_ttwid_webid(self, req_url):
        while True:
            try:
                headers = {
                    "User-Agent": self.user_agent,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
                }

                response = requests.request("GET", req_url, headers=headers, verify=False, timeout=3)
                cookies_dict = response.cookies.get_dict()
                ttwid_str = cookies_dict.get('ttwid')
                render_data_text = \
                re.compile('\<script id=\"RENDER_DATA\" type\=\"application\/json\">(.*?)\<\/script\>').findall(
                    response.text)
                if(render_data_text):
                    render_data_text=render_data_text[0]
                    render_data_text = requests.utils.unquote(render_data_text)
                    render_data_json = json.loads(render_data_text, strict=False)
                    webid = render_data_json.get('app').get('odin').get('user_unique_id')
                    return ttwid_str, webid
            except (
                requests.exceptions.ProxyError, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
                logging.error(e)
                time.sleep(1)