-- 用户账号
DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id`          INT          NOT NULL AUTO_INCREMENT,
  `user_name`   VARCHAR(256) NULL,
  `user_email`  VARCHAR(256) NOT NULL,
  `user_pwd`    VARCHAR(256) NULL,
  `user_right`  BIGINT       NOT NULL DEFAULT 0,
  `user_type`   INT          NOT NULL DEFAULT 0,
  `create_time` TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `desc`        VARCHAR(256) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_email` (`user_email`)
)
  DEFAULT CHARSET = utf8;
INSERT INTO users (user_name, user_email, user_pwd, user_right, user_type)
VALUES ('李艳国', 'lyg@meitu.com', 'e10adc3949ba59abbe56e057f20f883e', 1, 1);

-- 服务列表
DROP TABLE IF EXISTS `services`;
CREATE TABLE IF NOT EXISTS `services` (
  `id`            INT           NOT NULL AUTO_INCREMENT,
  `user_email`    VARCHAR(256)  NOT NULL,
  `service_name`  VARCHAR(128)  NOT NULL,
  `machine_id`    INTEGER       NOT NULL,
  `start_cmd`     VARCHAR(4096) NOT NULL,
  `stop_cmd`      VARCHAR(4096) NOT NULL,
  `is_active`     INT           NOT NULL DEFAULT 0,
  `auto_recover`  INT           NOT NULL DEFAULT 1,
  `mail_receiver` VARCHAR(1024) NOT NULL DEFAULT 'adtech@meitu.com',
  `create_time`   TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `desc`          VARCHAR(256)  NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `service_idx` (`service_name`),
  INDEX `machine_id` (machine_id)
)
  DEFAULT CHARSET = utf8;

-- 命令列表
DROP TABLE IF EXISTS `check_cmd`;
CREATE TABLE IF NOT EXISTS `check_cmd` (
  `id`          INT           NOT NULL AUTO_INCREMENT,
  `service_id`  INT           NOT NULL,
  `local_check` INT           NOT NULL DEFAULT 0,
  `check_shell` VARCHAR(4096) NOT NULL,
  `operator`    VARCHAR(64)   NOT NULL,
  `check_value` VARCHAR(256)  NOT NULL,
  `good_match`  INT           NOT NULL DEFAULT 0,
  `desc`        VARCHAR(256)  NULL,
  PRIMARY KEY (`id`)
)
  DEFAULT CHARSET = utf8;

-- 比较操作符
DROP TABLE IF EXISTS `operators`;
CREATE TABLE IF NOT EXISTS `operators` (
  `id`       INT         NOT NULL AUTO_INCREMENT,
  `operator` VARCHAR(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `operator` (`operator`)
)
  DEFAULT CHARSET = utf8;
INSERT INTO `operators` (operator) VALUES ('>'), ('>='), ('<'), ('<='), ('=='), ('include'), ('exclude');

-- 依赖关系
DROP TABLE IF EXISTS `service_rely`;
CREATE TABLE IF NOT EXISTS `service_rely` (
  `id`          INT          NOT NULL AUTO_INCREMENT,
  `service_id`  INT          NOT NULL,
  `rely_id`     INT          NOT NULL,
  `create_time` TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `desc`        VARCHAR(256) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `rely` (`service_id`, `rely_id`)
)
  DEFAULT CHARSET = utf8;

-- 机器列表
DROP TABLE IF EXISTS `machines`;
CREATE TABLE IF NOT EXISTS `machines` (
  `id`          INT          NOT NULL AUTO_INCREMENT,
  `ssh_user`    VARCHAR(128) NOT NULL,
  `ssh_ip`      VARCHAR(64)  NOT NULL,
  `ssh_port`    VARCHAR(32)  NOT NULL,
  `create_time` TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `desc`        VARCHAR(256) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `rely` (`ssh_user`, `ssh_ip`, `ssh_port`)
)
  DEFAULT CHARSET = utf8;

-- 服务状态
DROP TABLE IF EXISTS `monitor_status`;
CREATE TABLE IF NOT EXISTS `monitor_status` (
  `id`         INT NOT NULL AUTO_INCREMENT,
  `service_id` INT NOT NULL,
  `healthy`    INT NOT NULL,
  PRIMARY KEY (`id`)
)
  DEFAULT CHARSET = utf8;
;

-- 检测命令状态
DROP TABLE IF EXISTS `check_cmd_status`;
CREATE TABLE IF NOT EXISTS `check_cmd_status` (
  `id`           INT NOT NULL AUTO_INCREMENT,
  `check_cmd_id` INT NOT NULL,
  `healthy`      INT NOT NULL,
  PRIMARY KEY (`id`)
)
  DEFAULT CHARSET = utf8;
;