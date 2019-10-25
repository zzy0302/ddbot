## bddbot

### 功能

- 查电费 - （此处有API接口，可看[下方详情](###API)）

  - 私聊查询

    ```电费 ```+宿舍楼宇房间号(eg. *电费 西南七 203* | *查电费 友园4 211* | *查电费 20 514*)

  - 群查询

    @bot +私聊内容即可（**一定要是@，复制无效**）

- 查百度 - （来自**[teac-your-baidu](https://github.com/luchenqun/teach-you-baidu)**）

  - 私聊查询

    ```百度```+要查询的东西(eg. *baidu 怎么上谷歌* |*百度 我要上推*)

  - 群查询

    @bot +私聊内容即可（**一定要是@，复制无效**）

- 查天气 - （使用[和风天气]( https://dev.heweather.com/docs/api/ )接口）

  - 私聊查询

    ```天气```+要查询的天气(eg. *天气 成都* |*天气 上海*)

  - 群查询

    @bot +私聊内容即可（**一定要是@，复制无效**）

- 查出行 - （来自韩主席的PR）

  - 私聊查询

    ```回城```+时间(可选)(eg. *回城* |*回城 15:30*)

  - 群查询

    @bot +私聊内容即可（**一定要是@，复制无效**）

### API

描述：

​		传入楼宇房间号信息，返回时间戳+剩余电量（具体爬虫代码可以看历史commit，现后端为历史commit结合[Chromepool](https://github.com/zzy0302/Chroomepool)完成，后端服务不在此项目文件内）

​		使用redis缓存保存3分钟内查询过的房间，调用量目前没有限制

​		本接口仅供参考，不确保准确性，仅支持四平和嘉定校区

- URL: 
```
	pc.washingpatrick.cn:2345
```
- URI: `/elec`

- parameter:

  |      | 可否为空 | 描述                                                 |
  | ---- | -------- | ---------------------------------------------------- |
  | room | No       | 楼宇+房间号，例如  西南七203 （中文注意要urlencode） |
  | o    | Yes      | 为1时只返回电量值，不返回时间戳                      |
  | ..   | ..       | ..                                                   |

- 举例：

  - 带时间戳：![image-20191025170706504](https://github.com/zzy0302/ddbot/img/image-20191025170706504.png)

    

  - 不带时间戳：![image-20191025170541342](https://github.com/zzy0302/ddbot/img/image-20191025170541342.png)

