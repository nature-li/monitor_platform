// 错误提示框
$.showErr = function (str, func) {
    BootstrapDialog.show({
        type: BootstrapDialog.TYPE_DANGER,
        title: '错误 ',
        message: str,
        size: BootstrapDialog.SIZE_SMALL,
        draggable: true,
        buttons: [{
            label: '关闭',
            action: function (dialogItself) {
                dialogItself.close();
            }
        }],
        onhide: func
    });
};

// 警告提示框
$.showWarn = function (str, func) {
    BootstrapDialog.show({
        type: BootstrapDialog.TYPE_WARNING,
        title: '错误 ',
        message: str,
        size: BootstrapDialog.SIZE_SMALL,
        draggable: true,
        buttons: [{
            label: '关闭',
            action: function (dialogItself) {
                dialogItself.close();
            }
        }],
        onhide: func
    });
};

// 确认对话框
$.showConfirm = function (str, func_ok, func_close) {
    BootstrapDialog.show({
        title: '确认',
        message: str,
        cssClass: 'bootstrap_center_dialog',
        type: BootstrapDialog.TYPE_PRIMARY,
        size: BootstrapDialog.SIZE_SMALL,
        draggable: true,
        closable: false,
        buttons: [{
            label: '取消',
            action: function (dialogItself) {
                dialogItself.close();
            }
        }, {
            label: '确定',
            cssClass: 'btn-primary',
            action: function (dialogItself) {
                dialogItself.close();
                func_ok();
            }
        }],
        onhide: func_close,
    });
};

// Init select menu for rely service
function init_rely_service_select() {
    $.ajax({
            url: '/api_query_monitor_base',
            data: {
                'service_name': '',
                'off_set': 0,
                'limit': -1,
            },
            type: 'post',
            dataType: 'json',
            success: function (response) {
                if (!response.success) {
                    return;
                }

                for (var i = 0; i < response.content.length; i++) {
                    var item = response.content[i];
                    var option = '<option value=' + item.id + '>' + item.service_name + '</option>';
                    $('#rely_service_select').append(option);
                }
                $('#rely_service_select').selectpicker('refresh');
            },
            error: function (jqXHR, textStatus, errorThrown) {
                if (jqXHR.status === 302) {
                    window.location.replace('/');
                } else {
                    $.showErr('发生错误')
                }
            },
        }
    );
}

// Init operator list
function init_operator_list() {
    $.ajax({
            url: '/api_query_all_operator',
            type: 'post',
            dataType: 'json',
            success: function (response) {
                if (!response.success) {
                    return;
                }

                window.save_data.operator_list = response.content
            },
            error: function (jqXHR, textStatus, errorThrown) {
                if (jqXHR.status === 302) {
                    window.location.replace('/');
                } else {
                    $.showErr('发生错误')
                }
            },
        }
    );
}

// Init machine list
function init_machine_list() {
    $.ajax({
            url: '/api_query_machine',
            type: 'post',
            data: {
                'machine': '',
                'off_set': 0,
                'limit': -1
            },
            dataType: 'json',
            success: function (response) {
                if (!response.success) {
                    return;
                }

                for (var i = 0; i < response.content.length; i++) {
                    var item = response.content[i];
                    var option = '<option value=' + item.id + '>' + item.ssh_user + '@' + item.ssh_ip + ':' + item.ssh_port + '</option>';
                    $('#service_manager_select').append(option);
                }
                $('#service_manager_select').selectpicker('refresh');

            },
            error: function (jqXHR, textStatus, errorThrown) {
                if (jqXHR.status === 302) {
                    window.location.replace('/');
                } else {
                    $.showErr('发生错误')
                }
            },
        }
    );
}