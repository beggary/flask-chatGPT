function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    if (username === "") {
        alert("请输入内容！");
    } else {
        $.ajax({
            type: "POST",
            url: "/login_in",
            data: {"username": username, "password": password},
            success: function (response) {
                if (response.message === "ok") {
                    window.location = "index";
                } else if (response.message === "fail") {
                    alert("用户名或密码错误！")
                }
            },
            error: function (jqXHR) {
                alert("未知错误！" + jqXHR.status)
            },
            complete: function () {
            }
        });
    }
}

function haveKeyPage() {
    window.location.href = "/KeyPage";
}