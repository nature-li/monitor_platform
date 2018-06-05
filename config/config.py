#!/usr/bin/env python2.7
# coding: utf-8
from py_log.logger import LogEnv

# 日志配置
server_log_env = LogEnv.develop
server_log_target = "logs"
server_log_name = "platform"
server_log_size = 100 * 1024 * 1024
server_log_count = 100

# 服务配置
server_listen_port = 8888
server_debug_mode = True
server_cookie_secret = "write_your_own_password"
server_expire_time = 30 * 60

# OAUTH登录
server_oauth_app_id = ''
server_oauth_app_secret = ''
server_oauth_redirect_url = ''
server_oauth_token_url = ""
server_oauth_user_url = ""
server_oauth_auth_url = ''

# MySQL数据库配置
mysql_host = '127.0.0.1'
mysql_port = 3306
mysql_user = 'root'
mysql_pwd = '123456'
mysql_db = 'monitor'


# 监控服务地址
monitor_server_url = 'http://127.0.0.1:12345'

# Fake info
server_local_fake = True
