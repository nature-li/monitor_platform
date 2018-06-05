#!/usr/bin/env python2.7
# coding: utf-8

import requests
import traceback
from py_log.logger import Logger
from config import config


class Login(object):
    @classmethod
    def get_access_token(cls, code):
        try:
            a_dict = {
                'code': code,
                'appid': config.server_oauth_app_id,
                'appsecret': config.server_oauth_app_secret,
                'redirect_uri': config.server_oauth_redirect_url,
                'grant_type': 'auth_code',
            }
            r = requests.post(config.server_oauth_token_url, a_dict)
            if r.status_code != 200:
                Logger.error("get_access_token error, status_code[%s], content[%s]" % (r.status_code, r.content))
            return r.status_code, r.content
        except:
            Logger.error(traceback.format_exc())
            return None, None

    @classmethod
    def get_user_info(cls, token, open_id):
        try:
            a_dict = {
                'access_token': token,
                'appid': config.server_oauth_app_id,
                'openid': open_id
            }
            r = requests.post(config.server_oauth_user_url, a_dict)
            if r.status_code != 200:
                Logger.error("get_user_info error, status_code[%s], content[%s]" % (r.status_code, r.content))
            return r.status_code, r.content
        except:
            Logger.error(traceback.format_exc())
            return None, None
