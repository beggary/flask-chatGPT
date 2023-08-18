# flask-chatGPT
基于flask框架的chatGPT—API调用项目
1. 用户登录版：没有数据库，添加用户在服务端。
   * 包含免登录页面，用户可通过输入自己的APIkey实现chatGPT使用
     * 因为无法判断key的有效性，所以直接返回openai自身的报文。
2. 无需登录版：去除鉴权部分，跳转index就可以了。
   * 错误报文自己定义，用于控制多轮聊天次数，避免token消耗或轮询内容累计过多（可以显示maxtoken但很影响体验）、免费apikey的限制提示。
