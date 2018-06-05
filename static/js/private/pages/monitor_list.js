$(document).ready(function () {
    // 定义全局变量
    if (!window.save_data) {
        reset_save_data();
    }

    // 查询全部用户并更新列表
    query_and_update_view();

    // 定时任务
    setInterval(reload_monitor_status, 1000);
});

// 初始化全局变量
function reset_save_data() {
    window.save_data = {
        'item_list': [],
        'db_total_item_count': 0,
        'db_return_item_count': 0,
        'db_max_page_idx': 0,
        'view_max_page_count': 5,
        'view_item_count_per_page': 10,
        'view_start_page_idx': 0,
        'view_current_page_idx': 0,
        'view_current_page_count': 0,
    };
}

// 查询数据并更新页面
function query_and_update_view() {
    var off_set = window.save_data.view_current_page_idx * window.save_data.view_item_count_per_page;
    var limit = window.save_data.view_item_count_per_page;

    $.ajax({
            url: '/api_query_monitor',
            type: "post",
            data: {
                'service_name': $("#search_service_name").val(),
                'off_set': off_set,
                'limit': limit
            },
            dataType: 'json',
            success: function (response) {
                save_data_and_update_page_view(response);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                if (jqXHR.status == 302) {
                    window.location.replace("/");
                } else {
                    $.showErr("查询失败");
                }
            }
        }
    );
}

function query_and_update_view_silent() {
    var off_set = window.save_data.view_current_page_idx * window.save_data.view_item_count_per_page;
    var limit = window.save_data.view_item_count_per_page;

    $.ajax({
            url: '/api_query_monitor',
            type: "post",
            data: {
                'service_name': $("#search_service_name").val(),
                'off_set': off_set,
                'limit': limit
            },
            dataType: 'json',
            success: function (response) {
                save_data_and_update_page_view(response);
            },
        }
    );
}

// 更新页表
function update_page_view(page_idx) {
    // 删除表格
    $('#service_list_result > tbody  > tr').each(function () {
        $(this).remove();
    });

    // 添加表格
    for (var i = 0; i < window.save_data.item_list.length; i++) {
        var service = window.save_data.item_list[i];
        add_row(service);
    }
    $("[data-toggle='tooltip']").tooltip();

    // 更新分页标签
    update_page_partition(page_idx);
}

function get_img_from_healthy_code(healthy_code) {
    var img = '<img src="/static/images/white.png" alt="no data">';
    if (healthy_code === 1) {
        img = '<img src="/static/images/green.png" alt="success">';
    } else if (healthy_code === 2) {
        img = '<img src="/static/images/yellow.png" alt="warning">';
    } else if (healthy_code === 3) {
        img = '<img src="/static/images/red.png" alt="error">';
    }
    return img;
}

// 在表格中增加用户
function add_row(service) {
    var toggle_status = '否';
    var toggle_active = '<button type="button" class="btn btn-default btn-xs monitor-play-button" data-toggle="tooltip" title="点我恢复监测">' +
        '<span class="glyphicon glyphicon-play"></span></button>';
    if (service.is_active) {
        toggle_status = '是';
        toggle_active = '<button type="button" class="btn btn-default btn-xs monitor-pause-button" data-toggle="tooltip" title="点我暂停监测">' +
            '<span class="glyphicon glyphicon-pause"></span></button>';
    }

    var img = get_img_from_healthy_code(service.healthy_code);
    var table = $("#service_list_result");
    var manager = service.ssh_user + '@' + service.ssh_ip + ':' + service.ssh_port;
    var tr = $('<tr>' +
        '<td style="text-align:center;">' + service.id + '</td>' +
        '<td style="text-align:center;">' + service.user_email + '</td>' +
        '<td style="text-align:center;">' + service.service_name + '</td>' +
        '<td style="text-align:center;">' + manager + '</td>' +
        '<td style="text-align:center">' + toggle_status + '</td>' +
        '<td style="text-align:center">' + toggle_active + '</td>' +
        '<td style="text-align:center;">' + service.monitor_time + '</td>' +
        '<td style="text-align:center;">' + img + '</td>' +
        '<td style="text-align:center;"><button type="button" class="btn btn-default btn-xs monitor-view-button">查看</button></td>' +
        '<td style="text-align:center;"><button type="button" class="btn btn-default btn-xs monitor-edit-button">编辑</button></td>'
    );
    table.append(tr);
}

// 点击查找用户按钮
$(document).on("click", "#search_user_name_btn", function (e) {
    // 清空数据并设置查找账号
    reset_save_data();

    // 查询数据并更新页面
    query_and_update_view();
});


// 增加监测
$(document).on('click', '#add_service_button', function (e) {
    window.location.replace('/add_monitor');
});

// 暂停监测
$(document).on('click', '.monitor-pause-button', function (e) {
    var service_id = $(this).closest('tr').find('td:eq(0)').text();
    var expect_active = 0;
    async_set_monitor_active(service_id, expect_active);
});

// 激活监测
$(document).on('click', '.monitor-play-button', function (e) {
    var service_id = $(this).closest('tr').find('td:eq(0)').text();
    var expect_active = 1;
    async_set_monitor_active(service_id, expect_active);
});

function async_set_monitor_active(service_id, expect_active) {
    $.ajax({
            url: '/api_set_monitor_active',
            data: {
                'service_id': service_id,
                'expect_active': expect_active,
            },
            type: 'post',
            dataType: 'json',
            success: function (response) {
                if (!response.success) {
                    $.showErr("更新失败");
                    return;
                }

                var content = response.content;
                if (content.length === 0) {
                    window.location.reload();
                    return;
                }


                // Refresh monitor row
                var a_service = content[0];
                refresh_monitor_row(a_service)
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


function refresh_monitor_row(service) {
    $('#service_list_result > tbody > tr').each(function () {
        var page_service_id = $(this).find("td:eq(0)").text();
        if (page_service_id === service.id.toString()) {
            var toggle_status = '否';
            var toggle_active = '<button type="button" class="btn btn-default btn-xs monitor-play-button" data-toggle="tooltip" title="点我恢复监测">' +
                '<span class="glyphicon glyphicon-play"></span></button>';
            if (service.is_active) {
                toggle_status = '是';
                toggle_active = '<button type="button" class="btn btn-default btn-xs monitor-pause-button" data-toggle="tooltip" title="点我暂停监测">' +
                    '<span class="glyphicon glyphicon-pause"></span></button>';
            }

            var manager = service.ssh_user + '@' + service.ssh_ip + ':' + service.ssh_port;
            var img = get_img_from_healthy_code(service.healthy_code);
            $(this).find('td:eq(1)').html(service.user_email);
            $(this).find('td:eq(2)').html(service.service_name);
            $(this).find('td:eq(3)').html(manager);
            $(this).find('td:eq(4)').html(toggle_status);
            $(this).find('td:eq(5)').html(toggle_active);
            $(this).find('td:eq(6)').html(service.monitor_time);
            $(this).find('td:eq(7)').html(img);

            $("[data-toggle='tooltip']").tooltip();
        }
    });
}

$(document).on('click', '.monitor-view-button', function (e) {
    var service_id = $(this).closest('tr').find('td:eq(0)').text();
    var url = '/view_monitor?service_id=' + service_id;
    window.location.replace(url);
});

$(document).on('click', '.monitor-edit-button', function (e) {
    var service_id = $(this).closest('tr').find('td:eq(0)').text();
    var url = '/edit_monitor_detail?service_id=' + service_id;
    window.location.replace(url);
});

function reload_monitor_status() {
    query_and_update_view_silent();
}