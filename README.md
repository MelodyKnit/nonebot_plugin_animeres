# 动漫资源获取插件

这个插件主要是网站爬取过来的数据，在使用命令进行搜索时候采用关键字的方式，比如`天气之子`这时搜索的是`天气之子`相关资源，如果获取的资源并不理想或者你只需要生肉（无字幕）资源时，你就需要用`天气之子 raw`或`天气之子 mkv`这种多个关键字空格方式进行获取，这种方式准确度会比直接用`天气之子`精准且效果好，建议采用多关键字的方式进行搜索。

## 安装

`nb plugin install nonebot-plugin-animeres`

<details>
  <summary>使用pip安装</summary>

  `pip install nonebot-plugin-animeres`
</details>

- 命令
  - `资源`、`动漫资源`
- 参数
  - `资源名称`

## 配置参数

```env
ANIMERES_PROXY=""                      # 设置代理端口
ANIMERES_SITE=""                       # 选择资源站点
ANIMERES_FORWARD=false                 # 合并转发的形式发送消息
ANIMERES_LENGTH=3                      # 每次发送的数量，用-1表示全部取出
ANIMERES_FORMANT="{title}\n{magnet}"   # 发送的消息格式化
ANIMERES_ONESKIP=true                  # 当只有一个选项时跳过
ANIEMRES_PRIORITY=100

```

### ANIMERES_PROXY

通过`ANIMERES_PROXY`参数可以设置代理来加速资源的获取或者获取不到的情况

### ANIMERES_FORWARD

用来发送合并消息

![合并消息转发](image/forward.png)

### ANIMERES_FORMANT

格式化字符串

| 标签 | 说明 |
|---|---|
| title | 资源名称 |
| tag | 资源标签类型 |
| size | 资源大小 |
| magnet | 种子链接 |
