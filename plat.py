#!/usr/bin/env python2.7
# coding: utf-8
from gevent import monkey; monkey.patch_all()
import os.path
import sys
import json
import logging
import time
from urllib import quote
import datetime
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.log
from tornado.options import options
import requests

from config import config
from py_log.logger import Logger
from py_db.db_operate import DbOperator
from login.login import Login


class UserRight(object):
    USER_MANAGER = 0B00000001


class LoginUser(object):
    def __init__(self, user_email, user_name, pin_nav, pin_lock, user_right):
        """
        :type user_email: str
        :type user_name: str
        :type pin_nav: str
        :type pin_lock: str
        :type user_right: str
        """
        self.user_email = user_email
        """:type: string"""
        self.user_name = user_name
        """:type: string"""
        self.pin_nav = 1 if pin_nav == '1' else 0
        """:type: int"""
        self.pin_lock = 1 if pin_lock == '1' else 0
        """:type: int"""
        self.user_right = int(user_right) if user_right else 0
        """:type: int"""


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user_email")

    def get_login_user(self):
        try:
            # is_login
            user_email = self.current_user
            if not user_email:
                self.redirect("/login")
                return None
            user_email = tornado.escape.xhtml_escape(user_email)

            # user_name
            user_name = self.get_secure_cookie('user_name')
            if not user_name:
                self.redirect("/login")
                return None
            user_name = tornado.escape.xhtml_escape(user_name)

            # user_right
            user_right = self.get_secure_cookie('user_right')
            if not user_right:
                self.redirect('/login')
                return None
            user_right = tornado.escape.xhtml_escape(user_right)

            # last_time
            str_login_time = self.get_secure_cookie('last_time')
            if not str_login_time:
                self.redirect("/login")
                return None
            str_login_time = tornado.escape.xhtml_escape(str_login_time)

            # is expire
            now = time.time()
            last_time = float(str_login_time)
            time_span = now - last_time
            if time_span > config.server_expire_time:
                self.redirect("/login")
                return None

            # set last_time every 60 seconds
            if time_span > 60:
                self.set_secure_cookie("last_time", str(time.time()), expires_days=None)

            # get pin_nav
            pin_nav = self.get_cookie('pin_nav')
            if pin_nav:
                pin_nav = tornado.escape.xhtml_escape(pin_nav)

            # get pin_lock
            pin_lock = self.get_cookie('pin_lock')
            if pin_lock:
                pin_lock = tornado.escape.xhtml_escape(pin_lock)

            user = LoginUser(
                user_email=user_email,
                user_name=user_name,
                pin_nav=pin_nav,
                pin_lock=pin_lock,
                user_right=user_right
            )

            # 返回用户信息
            return user
        except:
            self.redirect("/login")
            return None


class IndexHandler(BaseHandler):
    def get(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        Logger.info(json.dumps(self.request.arguments, ensure_ascii=False), self.request.uri)
        self.redirect('/monitor_list')


class RefuseHandler(BaseHandler):
    def get(self):
        self.render('refuse.html')


class PageNotFoundHandler(BaseHandler):
    def get(self):
        self.render('404.html')


class UserListHandler(BaseHandler):
    def get(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        Logger.info(json.dumps(self.request.arguments, ensure_ascii=False), self.request.uri)
        if not login_user.user_right & UserRight.USER_MANAGER:
            self.redirect("/")
        self.render('user/user_list.html', login_user=login_user)


class MachineListHandler(BaseHandler):
    def get(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        Logger.info(json.dumps(self.request.arguments, ensure_ascii=False), self.request.uri)
        self.render('machine/machine_list.html', login_user=login_user)


class AddUserHandler(BaseHandler):
    def post(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        if not login_user.user_right & UserRight.USER_MANAGER:
            self.redirect("/")
        user_email = self.get_argument("user_email")
        user_right = self.get_argument("user_right")
        text = DbOperator.add_one_user(user_email, user_right)
        self.write(text)


class QueryUserListHandler(BaseHandler):
    def post(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        Logger.info(json.dumps(self.request.arguments, ensure_ascii=False), self.request.uri)
        if not login_user.user_right & UserRight.USER_MANAGER:
            self.redirect("/")
        user_email = self.get_argument("user_email")
        off_set = self.get_argument("off_set")
        limit = self.get_argument("limit")
        text = DbOperator.query_user_list(user_email, off_set, limit)
        self.write(text)


class ApiQueryMachineHandler(BaseHandler):
    def post(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        Logger.info(json.dumps(self.request.arguments, ensure_ascii=False), self.request.uri)
        if not login_user.user_right & UserRight.USER_MANAGER:
            self.redirect("/")
        user_email = self.get_argument("machine")
        off_set = self.get_argument("off_set")
        limit = self.get_argument("limit")
        text = DbOperator.query_machine_list(user_email, off_set, limit)
        self.write(text)


class ApiAddMachineHandler(BaseHandler):
    def post(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        if not login_user.user_right & UserRight.USER_MANAGER:
            self.redirect("/")
        ssh_user = self.get_argument("ssh_user")
        ssh_ip = self.get_argument("ssh_ip")
        ssh_port = self.get_argument("ssh_port")
        text = DbOperator.add_one_machine(ssh_user, ssh_ip, ssh_port)
        self.write(text)


class ApiEditMachineHandler(BaseHandler):
    def post(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        Logger.info(json.dumps(self.request.arguments, ensure_ascii=False), self.request.uri)
        machine_id = self.get_argument("machine_id")
        ssh_user = self.get_argument("ssh_user")
        ssh_ip = self.get_argument("ssh_ip")
        ssh_port = self.get_argument("ssh_port")
        text = DbOperator.edit_machine(machine_id, ssh_user, ssh_ip, ssh_port)
        self.write(text)


class ApiDeleteMachineHandler(BaseHandler):
    def post(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        Logger.info(json.dumps(self.request.arguments, ensure_ascii=False), self.request.uri)
        machine_id_list = self.get_argument("machine_id_list")
        text = DbOperator.delete_machines(machine_id_list)
        self.write(text)


class ApiDeleteOneMachine(BaseHandler):
    def post(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        Logger.info(json.dumps(self.request.arguments, ensure_ascii=False), self.request.uri)
        machine_id = self.get_argument("machine_id")
        text = DbOperator.delete_one_machine(machine_id)
        self.write(text)


class DeleteUserHandler(BaseHandler):
    def post(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        if not login_user.user_right & UserRight.USER_MANAGER:
            self.redirect("/")
        Logger.info(json.dumps(self.request.arguments, ensure_ascii=False), self.request.uri)
        user_id_list = self.get_argument("user_id_list")
        text = DbOperator.delete_users(user_id_list)
        self.write(text)


class EditUserHandler(BaseHandler):
    def post(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        if not login_user.user_right & UserRight.USER_MANAGER:
            self.redirect("/")
        Logger.info(json.dumps(self.request.arguments, ensure_ascii=False), self.request.uri)
        user_id = self.get_argument("user_id")
        user_right = self.get_argument("user_right")
        text = DbOperator.edit_user(user_id, user_right)
        self.write(text)


class MonitorListHandler(BaseHandler):
    def get(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        self.render('monitor/monitor_list.html', login_user=login_user)


class AddMonitorHandler(BaseHandler):
    def get(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        self.render('monitor/add_monitor.html', login_user=login_user)


class EditMonitorHandler(BaseHandler):
    def get(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        self.render('monitor/edit_monitor.html', login_user=login_user)


class ViewMonitorHandler(BaseHandler):
    def get(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        Logger.info(json.dumps(self.request.arguments, ensure_ascii=False), self.request.uri)
        service_id = self.get_argument('service_id')
        monitor_detail = DbOperator.query_monitor_detail(service_id)
        if not monitor_detail:
            self.redirect('/')
            return
        self.render('monitor/view_monitor.html',
                    login_user=login_user,
                    base=monitor_detail.base_info,
                    healthy=monitor_detail.healthy_check_list,
                    unhealthy=monitor_detail.unhealthy_check_list,
                    rely=monitor_detail.rely_service_list)


class QueryMonitorHandler(BaseHandler):
    def post(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        Logger.info(json.dumps(self.request.arguments, ensure_ascii=False), self.request.uri)
        service_name = self.get_argument("service_name")
        off_set = self.get_argument("off_set")
        limit = self.get_argument("limit")
        text = DbOperator.query_monitor_list(service_name, off_set, limit)
        self.write(text)


class QueryMonitorBaseHandler(BaseHandler):
    def post(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        service_name = self.get_argument("service_name")
        off_set = self.get_argument("off_set")
        limit = self.get_argument("limit")
        Logger.info(json.dumps(self.request.arguments, ensure_ascii=False), self.request.uri)
        text = DbOperator.query_all_monitor_base(service_name, off_set, limit)
        self.write(text)


class QueryAllOperatorHandler(BaseHandler):
    def post(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        Logger.info(json.dumps(self.request.arguments, ensure_ascii=False), self.request.uri)
        text = DbOperator.query_all_operator()
        self.write(text)


class ApiAddMonitorDetailHandler(BaseHandler):
    def post(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        Logger.info(json.dumps(self.request.arguments, ensure_ascii=False), self.request.uri)
        monitor_detail = self.get_argument('monitor_detail')
        text = DbOperator.insert_monitor_detail(login_user.user_email, monitor_detail)
        self.write(text)


class EditMonitorDetailHandler(BaseHandler):
    def get(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        Logger.info(json.dumps(self.request.arguments, ensure_ascii=False), self.request.uri)
        service_id = self.get_argument('service_id')
        monitor_detail = DbOperator.query_monitor_detail(service_id)
        all_rely = DbOperator.query_all_monitor_base_v2(service_id)
        all_machine = DbOperator.query_machine_list_v2()
        if monitor_detail is None or all_rely is None or all_machine is None:
            self.redirect('/')
            return
        self.render('monitor/edit_monitor.html',
                    login_user=login_user,
                    base=monitor_detail.base_info,
                    healthy=monitor_detail.healthy_check_list,
                    unhealthy=monitor_detail.unhealthy_check_list,
                    rely_id_set=set([item.id for item in monitor_detail.rely_service_list]),
                    all_rely=all_rely,
                    all_machine=all_machine)


class ApiEditMonitorDetailHandler(BaseHandler):
    def post(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        Logger.info(json.dumps(self.request.arguments, ensure_ascii=False), self.request.uri)
        service_id = self.get_argument('service_id')
        monitor_detail = self.get_argument('monitor_detail')
        text = DbOperator.edit_monitor_detail(login_user.user_email, service_id, monitor_detail)
        self.write(text)


class ApiDeleteMonitorDetailHandler(BaseHandler):
    def post(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        Logger.info(json.dumps(self.request.arguments, ensure_ascii=False), self.request.uri)
        service_id = self.get_argument('service_id')
        text = DbOperator.delete_monitor_detail(service_id)
        self.write(text)


class ApiSetMonitorActivelHandler(BaseHandler):
    def post(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        Logger.info(json.dumps(self.request.arguments, ensure_ascii=False), self.request.uri)
        service_id = self.get_argument('service_id')
        expect_active = self.get_argument('expect_active')
        text = DbOperator.set_monitor_active(service_id, expect_active)
        self.write(text)


class ApiGetJobFullStatusHandler(BaseHandler):
    def post(self):
        login_user = self.get_login_user()
        if not login_user:
            return
        Logger.info(json.dumps(self.request.arguments, ensure_ascii=False), self.request.uri)

        a_dict = dict()
        a_dict['code'] = -1
        a_dict['healthy_code'] = 0
        a_dict['command_healthy_code'] = dict()
        a_dict['monitor_time'] = '1970-01-01 00:00:00'

        # Check service id
        service_id = self.get_argument('service_id')
        if not service_id or not service_id.isdigit():
            self.write(json.dumps(a_dict, ensure_ascii=False))
            return

        url = config.monitor_server_url + '/api_get_detail_status'
        request_data = {
            'service_id': service_id,
        }
        r = requests.post(url, data=request_data)
        Logger.info("url=[%s], service_id=[%s], status_code=[%s], response=[%s]" % (url, service_id, r.status_code, r.text))
        if r.status_code != 200:
            self.write(json.dumps(a_dict, ensure_ascii=False))
            return
        json_dict = json.loads(r.text)
        self.write(json.dumps(json_dict, ensure_ascii=False))


class FakeLoginHandler(BaseHandler):
    def get(self):
        if config.server_local_fake:
            self.render("user/fake_login.html")

    def post(self):
        if config.server_local_fake:
            user_email = self.get_argument("user_email")
            db_user = DbOperator.get_user_info(user_email)
            if not db_user:
                self.render("user/fake_login.html")
                return
            self.set_secure_cookie("user_email", db_user.user_email, expires_days=None)
            self.set_secure_cookie("user_name", db_user.user_name, expires_days=None)
            self.set_secure_cookie("user_right", str(db_user.user_right), expires_days=None)
            self.set_secure_cookie("last_time", str(time.time()), expires_days=None)
            self.redirect("/")


class LoginAuthHandler(BaseHandler):
    def get(self):
        if config.server_local_fake:
            # 本机fake登录
            self.redirect('/fake_login')
            return

        # 线上真实登录
        Logger.info(json.dumps(self.request.arguments, ensure_ascii=False), self.request.uri)
        login_user = self.get_login_user()
        if login_user:
            self.redirect("/")
            return

        code_from_auth = self.get_argument('code', None)
        if not code_from_auth:
            redirect_url = config.server_oauth_auth_url
            redirect_url += '?appid=%s' % config.server_oauth_app_id
            redirect_url += '&response_type=code'
            redirect_url += '&redirect_uri=%s' % quote(config.server_oauth_redirect_url)
            redirect_url += '&scope=user_info'
            redirect_url += '&state=test'
            self.redirect(redirect_url)
            return

        status, content = Login.get_access_token(code_from_auth)
        if status != 200:
            self.write(content)
            return
        Logger.info("get_access_token: [%s]" % content)

        try:
            a_dict = json.loads(content)
        except:
            Logger.error("parse token error: content[%s]" % content)
            self.write(content)
            return

        access_token = a_dict.get("access_token", None)
        openid = a_dict.get("openid", None)
        status, content = Login.get_user_info(access_token, openid)
        if status != 200:
            self.write(content)
            return
        Logger.info("get_user_info: [%s]" % content)

        try:
            a_dict = json.loads(content)
        except:
            Logger.error("parse user_info error: contnet[%s]" % content)
            self.write(content)
            return

        user_name = a_dict.get("name")
        user_email = a_dict.get("email")
        db_user = DbOperator.get_user_info(user_email)
        if not db_user:
            self.redirect('/refuse')
            return

        # 保存session
        self.set_secure_cookie("user_email", user_email, expires_days=None)
        self.set_secure_cookie("user_name", user_name, expires_days=None)
        self.set_secure_cookie("user_right", str(db_user.user_right), expires_days=None)
        self.set_secure_cookie("last_time", str(time.time()), expires_days=None)

        # 重向定
        self.redirect("/")


class LogoutHandler(BaseHandler):
    def get(self):
        Logger.info(json.dumps(self.request.arguments, ensure_ascii=False), self.request.uri)
        self.clear_cookie("user_email")
        self.clear_cookie("user_name")
        self.clear_cookie("user_right")
        self.clear_cookie("last_time")
        self.set_status(302)
        self.redirect('/')


class ReloadHandler(BaseHandler):
    def get(self):
        Logger.info(json.dumps(self.request.arguments, ensure_ascii=False), self.request.uri)
        self.render('reload.html')


class LogFormatter(tornado.log.LogFormatter):
    def __init__(self):
        super(LogFormatter, self).__init__(
            fmt='%(color)s[%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(levelname)s]%(end_color)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )


def __main__():
    # 设置编码
    reload(sys)
    sys.setdefaultencoding('utf-8')

    # 解析参数
    options.parse_command_line()

    # 不要输出日志到屏幕
    logging.getLogger("tornado.access").propagate = False
    logging.getLogger("tornado.application").propagate = False
    logging.getLogger("tornado.general").propagate = False
    logging.getLogger("process").propagate = False
    logging.getLogger("report").propagate = False
    logging.getLogger("third").propagate = False

    # 初始化日志
    Logger.init(config.server_log_env, config.server_log_target, config.server_log_name, config.server_log_size,
                config.server_log_count)

    # 重定向tornado自带日志
    logging.getLogger("tornado.access").addHandler(Logger.get_third_handler())
    logging.getLogger("tornado.application").addHandler(Logger.get_third_handler())
    logging.getLogger("tornado.general").addHandler(Logger.get_third_handler())

    # 设置request日志
    logging.getLogger("requests").setLevel(logging.WARNING)

    print "server is starting..."
    Logger.info("server is starting...")
    Logger.info("config.server_listen_port: %s" % config.server_listen_port)

    app = tornado.web.Application(
        [
            (r'/', IndexHandler),
            (r'/fake_login', FakeLoginHandler),
            (r'/refuse', RefuseHandler),
            (r'/login', LoginAuthHandler),
            (r'/logout', LogoutHandler),
            (r'/user_list', UserListHandler),
            (r'/machine_list', MachineListHandler),
            (r'/api_add_user', AddUserHandler),
            (r'/api_del_user', DeleteUserHandler),
            (r'/api_edit_user', EditUserHandler),
            (r'/api_query_user', QueryUserListHandler),
            (r'/api_query_machine', ApiQueryMachineHandler),
            (r'/api_add_machine', ApiAddMachineHandler),
            (r'/api_edit_machine', ApiEditMachineHandler),
            (r'/api_del_machine', ApiDeleteMachineHandler),
            (r'/api_del_one_machine', ApiDeleteOneMachine),
            (r'/monitor_list', MonitorListHandler),
            (r'/add_monitor', AddMonitorHandler),
            (r'/edit_monitor', EditMonitorHandler),
            (r'/view_monitor', ViewMonitorHandler),
            (r'/api_query_monitor', QueryMonitorHandler),
            (r'/api_query_monitor_base', QueryMonitorBaseHandler),
            (r'/api_query_all_operator', QueryAllOperatorHandler),
            (r'/api_add_monitor_detail', ApiAddMonitorDetailHandler),
            (r'/api_set_monitor_active', ApiSetMonitorActivelHandler),
            (r'/edit_monitor_detail', EditMonitorDetailHandler),
            (r'/api_edit_monitor_detail', ApiEditMonitorDetailHandler),
            (r'/api_delete_monitor_detail', ApiDeleteMonitorDetailHandler),
            (r'/api_get_job_full_status', ApiGetJobFullStatusHandler),
            ('.*', PageNotFoundHandler)
        ],
        cookie_secret=config.server_cookie_secret,
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=False,
        debug=config.server_debug_mode
    )
    app.listen(config.server_listen_port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    __main__()
