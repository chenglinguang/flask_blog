function confirmDelete(blogId) {
    bootbox.confirm("确定删除？", function (result) {
        if (result) {
            $.post($SCRIPT_ROOT + "/delete/" + blogId, function () {
                window.location.href = $SCRIPT_ROOT + "/";
            });
        }
    });
}

