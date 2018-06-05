// Click add healthy check
function add_checker_cmd(table_body) {
    BootstrapDialog.show({
        message: function (dialog) {
            var content = '';

            // local execute
            content += '<div class="form-group">';
            content += '<label>本地执行以下命令:&nbsp&nbsp<input id="dlg_local_execute" type="checkbox" value="1" /></label>';
            content += '</div>';    // </form-group>

            // header
            content += '<div class="form-horizontal">';
            content += '<div class="form-group">';

            // input command
            content += '<div class="col-xs-8"><input id="dlg_input_cmd" type="text" maxlength="4096" class="form-control" placeholder="非空，请输入本地或远程执行命令"/></div>';

            // operator select
            content += '<div class="col-xs-2"><select id="dlg_operator_list" class="form-control">';
            for (var i = 0; i < window.save_data.operator_list.length; i++) {
                var item = window.save_data.operator_list[i];
                content += '<option>' + $('<div>').text(item.operator).html() + '</option>';
            }
            content += '</select></div>';

            // right value
            content += '<div class="col-xs-2"><input id="dlg_right_value" type="text" maxlength="256" class="form-control" placeholder="输入期望结果"></div>';

            // footer
            content += '</div>';    // </form-group>
            content += '</div>';    // </form-horizontal>
            return content;
        },
        size: BootstrapDialog.SIZE_WIDE,
        title: '增加健康检测',
        closable: false,
        draggable: true,
        buttons: [
            {
                label: '确定',
                action: function (dialogItself) {
                    var input_cmd = $("#dlg_input_cmd").val().trim();
                    if (!input_cmd) {
                        return
                    }

                    var right_value = $("#dlg_right_value").val().trim();
                    if (!right_value) {
                        return;
                    }

                    var row = '<tr>';   // row start
                    // id
                    row += '<td>0</td>';
                    // input_cmd start
                    row += '<td width="60%">' + input_cmd + '</td>';
                    // local input
                    if ($("#dlg_local_execute").prop('checked')) {
                        row += '<td>是</td>';
                    } else {
                        row += '<td>否</td>';
                    }
                    // operator
                    row += '<td>' + $("#dlg_operator_list").val() + '</td>';
                    // right value
                    row += '<td>' + right_value + '</td>';
                    // delete button
                    row += '<td><a class="link_for_healthy_edit"><span class="glyphicon glyphicon-edit"></span></a></td>';
                    row += '<td><a class="link_for_healthy_delete"><span class="glyphicon glyphicon-minus-sign"></span></a></td>';
                    row += '</tr>';

                    // append row to table
                    table_body.append(row);

                    // Set change status
                    window.have_been_changed = true;

                    dialogItself.close();
                },
            },
            {
                label: '取消',
                action: function (dialogItself) {
                    dialogItself.close();
                }
            }]
    });
};

// Click add healthy check
function edit_checker_cmd(table_tr) {
    var check_id = table_tr.find('td:eq(0)').text().trim();
    var check_cmd = table_tr.find('td:eq(1)').text().trim();
    var local_check = table_tr.find('td:eq(2)').text().trim();
    var operator = table_tr.find('td:eq(3)').text().trim();
    var check_value = table_tr.find('td:eq(4)').text().trim();
    BootstrapDialog.show({
        message: function (dialog) {
            var content = '';

            // local execute
            content += '<div class="form-group">';
            if (local_check === '否') {
                content += '<label>本地执行以下命令:&nbsp&nbsp<input id="dlg_local_execute" type="checkbox" value="1" /></label>';
            } else {
                content += '<label>本地执行以下命令:&nbsp&nbsp<input id="dlg_local_execute" type="checkbox" value="1" checked/></label>';
            }
            content += '</div>';    // </form-group>

            // header
            content += '<div class="form-horizontal">';
            content += '<div class="form-group">';

            // input command
            content += '<div class="col-xs-8"><input id="dlg_input_cmd" value="' + check_cmd + '"maxlength="4096" class="form-control" placeholder="非空，请输入本地或远程执行命令"/></div>';

            // operator select
            content += '<div class="col-xs-2"><select id="dlg_operator_list" class="form-control">';
            for (var i = 0; i < window.save_data.operator_list.length; i++) {
                var item = window.save_data.operator_list[i];

                if (item.operator === operator) {
                    content += '<option selected>' + $('<div>').text(item.operator).html() + '</option>';
                } else {
                    content += '<option>' + $('<div>').text(item.operator).html() + '</option>';
                }
            }
            content += '</select></div>';

            // right value
            content += '<div class="col-xs-2"><input id="dlg_right_value" value="' + check_value + '" maxlength="256" class="form-control" placeholder="输入期望结果"></div>';

            // footer
            content += '</div>';    // </form-group>
            content += '</div>';    // </form-horizontal>
            return content;
        },
        size: BootstrapDialog.SIZE_WIDE,
        title: '编辑健康检测',
        closable: false,
        draggable: true,
        buttons: [
            {
                label: '确定',
                action: function (dialogItself) {
                    var input_cmd = $("#dlg_input_cmd").val().trim();
                    if (!input_cmd) {
                        return
                    }

                    var right_value = $("#dlg_right_value").val().trim();
                    if (!right_value) {
                        return;
                    }

                    table_tr.find('td:eq(1)').html(input_cmd);
                    if ($("#dlg_local_execute").prop('checked')) {
                        table_tr.find('td:eq(2)').html('是');
                    } else {
                        table_tr.find('td:eq(2)').html('否');
                    }
                    table_tr.find('td:eq(3)').html($("#dlg_operator_list").val());
                    table_tr.find('td:eq(4)').html(right_value);

                    // Set change status
                    window.have_been_changed = true;

                    dialogItself.close();
                },
            },
            {
                label: '取消',
                action: function (dialogItself) {
                    dialogItself.close();
                }
            }]
    });
};

// Click add healthy check
$(document).on('click', '#btn_add_healthy_check', function (e) {
    var healthy_table = $("#tbl_body_healthy > tbody");
    add_checker_cmd(healthy_table);
});

// Click add unhealthy check
$(document).on('click', '#btn_add_unhealthy_check', function (e) {
    var unhealthy_table = $("#tbl_body_unhealthy > tbody");
    add_checker_cmd(unhealthy_table);
});

// Edit a row
$(document).on("click", ".link_for_healthy_edit", function (e) {
    var healthy_tr = $(this).closest('tr');
    // Edit change status
    edit_checker_cmd(healthy_tr);
    window.have_been_changed = true;
});

// Delete a row
$(document).on("click", ".link_for_healthy_delete", function (e) {
    $(this).closest('tr').remove();
    // Set change status
    window.have_been_changed = true;
});


// go to top
function go_to_top() {
    $('html,body').scrollTop(0);
}

// get check cmd
function get_check_cmd(tr_list, good_match) {
    var check_cmd_list = [];
    tr_list.each(function () {
        var id = $(this).find('td:eq(0)').text();
        var command = $(this).find('td:eq(1)').text();
        var local = $(this).find('td:eq(2)').text();
        var operator = $(this).find('td:eq(3)').text();
        var right_value = $(this).find('td:eq(4)').text();

        var is_local = false;
        if (local === '是') {
            is_local = true;
        }

        var one_check = {
            id: id,
            check_shell: command,
            local_check: is_local,
            operator: operator,
            check_value: right_value,
            good_match: good_match,
        };

        check_cmd_list.push(one_check);
    });

    return check_cmd_list;
}

// Get page detail
function get_page_detail() {
    var request = {};

    // Get base info
    var service_name = $("#service_name").val().trim();
    if (!service_name) {
        return null;
    }
    request['service_name'] = service_name;

    var machine_id = $("#service_manager_select").val().trim();
    if (!machine_id) {
        return null;
    }
    request['machine_id'] = machine_id;

    var auto_recover = $("#auto_recover").val().trim();
    if (!auto_recover) {
        return null;
    }
    request['auto_recover'] = parseInt(auto_recover);

    var start_cmd = $("#start_cmd").val().trim();
    if ((auto_recover === "1") && (!start_cmd)) {
        return null;
    }
    request['start_cmd'] = start_cmd;

    var stop_cmd = $("#stop_cmd").val().trim();
    if ((auto_recover === "1") && (!stop_cmd)) {
        return null;
    }
    request['stop_cmd'] = stop_cmd;

    var mail_receiver = $("#mail_receiver").val().trim();
    if (!mail_receiver) {
        return null;
    }
    request['mail_receiver'] = mail_receiver;

    var is_active = $("#is_activate").val().trim();
    if (!is_active) {
        return null;
    }
    request['is_active'] = parseInt(is_active);

    request['rely_service_list'] = $("#rely_service_select").val();

    // Get check cmd list
    var healthy_tr_list = $("#tbl_body_healthy > tbody > tr");
    var healthy_cmd_list = get_check_cmd(healthy_tr_list, 1);

    var unhealthy_tr_list = $("#tbl_body_unhealthy > tbody > tr");
    var unhealthy_cmd_list = get_check_cmd(unhealthy_tr_list, 0);

    var check_cmd_list = healthy_cmd_list.concat(unhealthy_cmd_list);
    if (check_cmd_list.length === 0) {
        $.showWarn('请添加条件检测命令');
        return null;
    }
    request['check_cmd_list'] = check_cmd_list;

    return request;
}