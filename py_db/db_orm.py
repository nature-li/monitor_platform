#!/usr/bin/env python2.7
# coding: utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, BigInteger, TIMESTAMP, UniqueConstraint
from sqlalchemy.sql import func

Base = declarative_base()


# 用户列表
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(255), nullable=True)
    user_email = Column(String(255), unique=True)
    user_pwd = Column(String(255), nullable=True)
    user_right = Column(Integer, default=0)
    user_type = Column(Integer, default=0)
    create_time = Column(TIMESTAMP, default=func.now())
    desc = Column(String(255), nullable=True)


# 监测列表
class Services(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String(255))
    service_name = Column(String(128))
    machine_id = Column(Integer)
    start_cmd = Column(String(4096))
    stop_cmd = Column(String(4096))
    is_active = Column(Integer, default=0)
    auto_recover = Column(Integer, default=1)
    mail_receiver = Column(String(1024), default='adtech@meitu.com')
    create_time = Column(TIMESTAMP, default=func.now())
    desc = Column(String(255), nullable=True)
    UniqueConstraint('service_name', 'ssh_ip')


# 执行命令
class CheckCmd(Base):
    __tablename__ = 'check_cmd'
    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(Integer)
    local_check = Column(Integer, default=0)
    check_shell = Column(String(4096))
    operator = Column(String(64))
    check_value = Column(String(64))
    good_match = Column(Integer, default=0)
    desc = Column(String(255), nullable=True)


# 操作符号
class Operator(Base):
    __tablename__ = 'operators'
    id = Column(Integer, primary_key=True, autoincrement=True)
    operator = Column(String(64))


# 依赖关系
class ServiceRely(Base):
    __tablename__ = 'service_rely'
    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(Integer)
    rely_id = Column(Integer)
    create_time = Column(TIMESTAMP, default=func.now())
    desc = Column(String(255), nullable=True)
    UniqueConstraint('service_id', 'rely_id')


# 机器列表
class Machines(Base):
    __tablename__ = 'machines'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ssh_user = Column(String(128))
    ssh_ip = Column(String(64))
    ssh_port = Column(Integer)
    create_time = Column(TIMESTAMP, default=func.now())
    desc = Column(String(255), nullable=True)
    UniqueConstraint('ssh_user', 'ssh_ip', 'ssh_port')
