from flask import Flask, render_template, request, Response
import openai
import urllib3
import time
import logging

app = Flask(__name__)
urllib3.disable_warnings()

# %%
openai.api_key = "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"
# openai.api_key = "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"
# %%
# os.environ["HTTPS_PROXY"] = '172.104.102.91:8080'
# os.environ['HTTPS_PROXY'] = 'http://185.160.26.114:80'

start_time = time.time()
logging.basicConfig(filename='app.log', level=logging.DEBUG)

messages = []


@app.route('/')
def index():
    global messages
    messages = []
    return render_template("index.html")


# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('404.html'), 404


@app.route('/chatGPT', methods=['POST'])
def chatGPT():
    inputText = request.json['inputText']
    messages.append({"role": "user", "content": inputText})
    qT = time.strftime("%Y-%m-%d_%H:%M:%S")
    print(messages)
    logging.debug("===========================")
    logging.debug("time: %s", qT)
    logging.debug("userIn: %s", inputText)
    logging.debug("===========================")
    if len(messages) < 10000:
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
                return Response("请求太过频繁，请稍后再试。", mimetype='text/event-stream',
                                headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})
    else:
        return Response("最多执行500轮连续对话，请刷新页面", mimetype='text/event-stream',
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
        # 将chatGPT的回答内容 添加到数组中去
        messages.append({"role": "assistant", "content": full_reply_content})
    return Response(generate(), mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})

