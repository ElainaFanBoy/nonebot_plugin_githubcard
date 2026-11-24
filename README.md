<div align="center">
  <a href="https://nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-githubcard

_✨ 检测GitHub仓库链接并自动发送卡片信息（支持 NoneBot2 多种适配器）✨_

<img src="https://img.shields.io/github/license/ElainaFanBoy/nonebot_plugin_githubcard.svg" alt="license">
<img src="https://img.shields.io/badge/nonebot-2.0.0+-red.svg" alt="NoneBot">
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>

## 📖 介绍

检测GitHub仓库链接并自动发送卡片信息。通过 `nonebot-plugin-alconna` 的通用消息组件发送图片，支持其已适配的多种 NoneBot2 适配器（具体取决于目标平台的图片消息支持情况）。

## 💿 安装

<details>
<summary>使用PIP安装</summary>


    pip install nonebot-plugin-githubcard
</details>

<details>
<summary>克隆至本地安装</summary>


    git clone https://github.com/ElainaFanBoy/nonebot_plugin_githubcard.git
</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| github_token | 否 | 无 | github_token = ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx |
| github_type | 否 | 0 | github图片样式(0为socialify样式，1为opengraph样式) |

## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 说明 |
|:-----:|:----:|:----:|:----:|
| https://github.com/xxx/xxx | 所有人 | 否 | GitHub仓库链接 |
### 效果图

<div align="left">
  
  socialify样式：
  
  <img src="https://socialify.git.ci/nonebot/nonebot2/png?description=1&font=Rokkitt&forks=1&issues=1&language=1&logo=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F63496654%3Fs%3D200%26v%3D4&name=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Light" width="600"/>
  
  opengraph样式：
  
  <img src="https://opengraph.githubassets.com/githubcard/nonebot/nonebot2" width="600"/>
</div>
