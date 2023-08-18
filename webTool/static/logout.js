    function logout() {
        if (confirm("确定要登出吗？")) {
// 使用Ajax发送POST请求
            $.ajax({
                type: "POST",
                url: "/logout",
                success: function (response) {
                    if (response.message === "ok") {
                        window.location = "index";
                    } else if (response.message === "fail") {
                        alert("用户未登录");
                    }
                },
                error: function (jqXHR) {
                    alert("未知错误！" + jqXHR.status);
                },
                complete: function () {
// 请求完成后执行的代码
                }
            });
        }
    }