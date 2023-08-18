from flask import Flask, render_template, request, Response, session  # 导入所需的Flask模块和函数
from werkzeug.security import generate_password_hash, check_password_hash
import openai
import urllib3
import time
import logging
import os
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)
urllib3.disable_warnings()
start_time = time.time()
# 配置根logger，将日志输出到app.log文件
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# 获取根logger实例
# root_logger = logging.getLogger()

# 创建一个FileHandler并设置编码为utf-8
file_handler = logging.FileHandler('app.log', encoding='utf-8')
api_key = [
    "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",
    "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",
    "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",
    "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",
    "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", ]

users = {
    'admin': {
        'username': 'admin',
        'password': generate_password_hash('admin666')  # 生成密码的哈希值
    },
    'yuxi': {
        'username': 'yuxi',
        'password': generate_password_hash('yuxi666')
    },
    'wenjia': {
        'username': 'wenjia',
        'password': generate_password_hash('wenjia666')
    },
    '2': {
        'username': '2',
        'password': generate_password_hash('2')
    },
    # ===========出售账号=================================
    'user010101': {
        'username': 'user010101',
        'password': generate_password_hash('EG7DY76T32672')
    },
    'user010102': {
        'username': 'user010102',
        'password': generate_password_hash('D2734R34F256G64')
    },
    'user010103': {
        'username': 'user010103',
        'password': generate_password_hash('4G46GR4324G456')
    },
    'user010104': {
        'username': 'user010104',
        'password': generate_password_hash('45G2465HB6UU76')
    },
    'user010105': {
        'username': 'user010105',
        'password': generate_password_hash('76N867J8J56H678J')
    },
    'user010106': {
        'username': 'user010106',
        'password': generate_password_hash('V456566H747J857H')
    },
}
app.config['SECRET_KEY'] = os.urandom(24)
user_messages = {}
key_messages = []


@app.route('/')
def index():
    if 'username' in session:  # 检查session中是否存在username
        user_messages[session['username']] = []
        return render_template('index_have_apikey.html')
    else:
        return render_template("login.html")


@app.route('/KeyPage')
def KeyPage():
    return render_template('index_have_apikey.html')


# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('404.html'), 404

@app.route('/index')
def star():
    if 'username' in session:  # 检查session中是否存在username
        user_messages[session['username']] = []
        return render_template('index_have_apikey.html')
    else:
        return render_template("login.html")


@app.route('/login_in', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    # 检查用户是否已从其他位置登录。
    if 'username' in session and session['username'] != username:
        return {"message": "Account logged in from another location!"}

    if username in users:
        if check_password_hash(users[username]['password'], password):
            session['username'] = username
            user_messages[username] = []
            openai.api_key = random.choice(api_key)
            return {'message': "ok"}
        else:
            return {"message": "fail"}
    return {"message": "fail"}


@app.route('/logout', methods=['POST'])
def logout():
    if 'username' in session:
        session.pop('username')
        return {'message': "ok"}
    else:
        # 就算用户不存在，也返回登录页
        return {'message': "fail"}


@app.route('/keyGPT', methods=['POST'])
def keyGPT():
    inputText = request.json['inputText']
    apikey = request.json['apikey']
    openai.api_key = apikey
    print(key_messages)
    key_messages.append({"role": "user", "content": inputText})
    if len(key_messages) < 10:
        try:
            if not openai.api_key:
                return Response("key不能为空", mimetype='text/event-stream',
                                headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})
            response_iter = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                # max_tokens=4000,
                messages=key_messages,
                stream=True
            )
        except Exception as e:
            if hasattr(e, "status_code") and e.status_code == 500:
                return Response(str(e), mimetype='text/event-stream',
                                headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})
            else:
                return Response(str(e), mimetype='text/event-stream',
                                headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})
    else:
        return Response("最多执行5轮连续对话，请刷新页面", mimetype='text/event-stream',
                        headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})

    def generate():
        # 创建并重置数组
        boot_messages = []
        for response in response_iter:
            message = response['choices'][0]['delta']
            clean = f"{''.join(message.get('content', ''))}"
            boot_messages.append(message)
            yield clean
        # 提取流式响应 回答内容
        full_reply_content = ''.join([m.get('content', '') for m in boot_messages])
        print(full_reply_content)
        logging.debug("===========================")
        logging.debug("time: %s", time.strftime("%Y-%m-%d_%H:%M:%S"))
        logging.debug("userIn: %s", inputText)
        logging.debug("chatgpt: %s", full_reply_content)
        logging.debug("===========================")
        # 将chatGPT的回答内容 添加到数组中去
        key_messages.append({"role": "assistant", "content": full_reply_content})
        # 以流式响应推送给前端

    return Response(generate(), mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})


@app.route('/chatGPT', methods=['POST'])
def chatGPT():
    if 'username' not in session:
        return {"message": "fail"}
    inputText = request.json['inputText']
    username = session['username']
    messages = user_messages[username]
    user_messages[username].append({"role": "user", "content": inputText})
    print(messages)
    if len(messages) < 10:
        try:
            response_iter = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                # max_tokens=4000,
                messages=messages,
                stream=True
            )
        except Exception as e:
            if hasattr(e, "status_code") and e.status_code == 500:
                return Response(str(e), mimetype='text/event-stream',
                                headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})
            else:
                return Response("请求太过频繁-限制：3/分钟。请在 20 秒后重试，如仍有问题联系我",
                                mimetype='text/event-stream',
                                headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})
    else:
        return Response("最多进行5轮连续对话，请刷新页面", mimetype='text/event-stream',
                        headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})

    def generate(user_name):
        # 创建并重置数组
        boot_messages = []
        for response in response_iter:
            message = response['choices'][0]['delta']
            clean = f"{''.join(message.get('content', ''))}"
            boot_messages.append(message)
            yield clean
        # 提取流式响应 回答内容
        full_reply_content = ''.join([m.get('content', '') for m in boot_messages])
        print(full_reply_content)
        logging.debug("===========================")
        qT = time.strftime("%Y-%m-%d_%H:%M:%S")
        logging.debug("time: %s", qT)
        logging.debug("userIn: %s", inputText)
        logging.debug("chatgpt: %s", full_reply_content)
        logging.debug("===========================")
        # 将chatGPT的回答内容 添加到数组中去
        user_messages[user_name].append({"role": "assistant", "content": full_reply_content})

    return Response(generate(username), mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})
