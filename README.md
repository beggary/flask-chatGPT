# flask-chatGPT
基于flask框架的chatGPT—API调用的简单项目
1. 用户登录版：下水道服务器，没接数据库，添加用户在服务端。
   * 包含免登录页面，用户可通过输入自己的APIkey实现chatGPT使用
     * 因为无法判断key的有效性，所以直接返回openai自身的报文。
    ![image](https://github.com/beggary/flask-chatGPT/assets/68416662/fbf90898-6388-4471-b0d1-8b83e6e28d0c)
2. 无需登录版：去除鉴权部分，跳转index就可以了。
   * 错误报文自己定义，用于控制多轮聊天次数，避免token消耗或轮询内容累计过多（可以显示maxtoken但很影响体验）、免费apikey的限制提示。
     ![image](https://github.com/beggary/flask-chatGPT/assets/68416662/a06a2366-31de-4e2c-bf5c-cb499ee42d45)
PS：
   1. 缺失代码高亮，前端这部分不会写.
