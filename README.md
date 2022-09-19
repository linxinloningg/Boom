**基于SMSBoom项目的增强和代码优化**

![logo](img/smsboom-logo.png)


## 原有Feature

1. 通过自定义 `api.json` 的方式定义接口.  
2. 支持关键字替换. **时间戳** `[timestamp]` **手机号** `[phone]`  
3. 多线程/异步 请求.  
4. 通过 Flask 提供网页测试/添加接口.  
5. 友好的命令行参数支持.  
6. ~~采用方便的 pipenv 包管理.~~  
7. ~~通过代理调用短信接口, 支持http, socks4, socks5代理.~~
8. 使用随机的User-Agent.
9. ~~可指定轰炸次数, 轰炸间隔时间.~~

## 增加Feature

1. 增加也可通过代理调用异步请求
2. 使用ProxyPool获取代理替换原有的读取代理接口文件获取代理
3. 更多的随机的User-Agent
4. 不再需要指定轰炸次数，只需指定间隔时间，即可实现循环轰炸，直到想停

## Quick Start

* ### 部署ProxyPool

  >* 克隆代码
  >
  >  ```bash
  >  git clone https://github.com/Python3WebSpider/ProxyPool.git
  >  cd ProxyPool
  >  ```
  >
  >* 使用 Docker
  >
  >  安装如下环境：
  >
  >  - Docker
  >  - Docker-Compose
  >
  >  安装方法自行搜索即可。
  >
  >  ```bash
  >  docker-compose up
  >  ```
  >
  >  运行结果类似如下：
  >
  >  ```bash
  >  redis        | 1:M 19 Feb 2020 17:09:43.940 * DB loaded from disk: 0.000 seconds
  >  redis        | 1:M 19 Feb 2020 17:09:43.940 * Ready to accept connections
  >  proxypool    | 2020-02-19 17:09:44,200 CRIT Supervisor is running as root.  Privileges were not dropped because no user is specified in the config file.  If you intend to run as root, you can set user=root in the config file to avoid this message.
  >  proxypool    | 2020-02-19 17:09:44,203 INFO supervisord started with pid 1
  >  proxypool    | 2020-02-19 17:09:45,209 INFO spawned: 'getter' with pid 10
  >  proxypool    | 2020-02-19 17:09:45,212 INFO spawned: 'server' with pid 11
  >  proxypool    | 2020-02-19 17:09:45,216 INFO spawned: 'tester' with pid 12
  >  proxypool    | 2020-02-19 17:09:46,596 INFO success: getter entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
  >  proxypool    | 2020-02-19 17:09:46,596 INFO success: server entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
  >  proxypool    | 2020-02-19 17:09:46,596 INFO success: tester entered RUNNING state, process has stayed up for > than 1 seconds (startsecs)
  >  ```
  >
  >  验证是否搭建成功，可访问 http://localhost:5555/random 即可获取一个随机可用代理
  >
  >  往后想要再次启动，只需要进入到ProxyPool代码文件夹，桥下命令
  >
  >  ```bash
  >  docker-compose start
  >  ```

* ## 部署Boom

  >* 克隆代码
  >
  >  ```bash
  >  git clone https://github.com/linxinloningg/Boom.git
  >  ```
  >
  >* 配置环境
  >
  >  **前提条件:** 请确保自己的电脑有 `python3.x` 的环境,推荐使用 `3.8` 及以上!  
  >
  >  推荐使用conda虚拟环境
  >
  >  ```bash
  >  # 创建新的虚拟环境
  >  conda create -n boom python=3.8
  >  ```
  >
  >  ```bash
  >  # 激活虚拟环境
  >  conda activate boom
  >  # 下载依赖
  >  cd Boom
  >  pip install -r requirements.txt
  >  ```
  >
  >* 尝试启动
  >
  >  ```bash
  >  python main.py
  >  ```
  >
  >  前端测试api界面
  >
  >  ```bash
  >  python run_flask_app.py start
  >  ```

### 开启轰炸  

帮助信息:

```shell
PS C:\Users\Administrator\Desktop\Boom> python .\main.py  

Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  async-run  以最快的方式请求接口(真异步百万并发)
  one-run    单线程(测试使用)
  run        传入线程数和手机号启动轰炸,支持多手机号
  update     从 github 获取最新接口
```

* ### run

```shell
PS C:\Users\Administrator\Desktop\Boom> python .\main.py run --help
Usage: main.py run [OPTIONS]

  传入线程数和手机号启动轰炸,支持多手机号

Options:
  -t, --thread INTEGER    线程数(默认64)
  -p, --phone TEXT        手机号,可传入多个再使用-p传递  [required]
  -i, --interval INTEGER  间隔时间(默认60s)
  -e, --proxies INTEGER   一次攻击所需代理(默认10),不使用代理则设为0
  --help                  Show this message and exit.
```

>### 命令示例
>
>启动64个线程,轰//炸一个人的手机号(198xxxxxxxx),不使用代理
>
>```shell
>python main.py run -t 64 -p 198xxxxxxxx -e 0
>```
>
>启动64个线程,轰//炸一个人的手机号(198xxxxxxxx),启动循环轰//炸,  每次间隔30秒
>
>```shell
>python smsboom.py run -t 64 -p 198xxxxxxxx -i 30 -e 0
>```
>
>启动64个线程,轰//炸一个人的手机号(198xxxxxxxx),启动循环轰//炸, 每次间隔30秒, 开启代理，每次轰炸在10个代理中随机选择一个代理搭配一个api，进行轰炸
>
>```shell
>python smsboom.py run -t 64 -p 198xxxxxxxx -f 60 -i 30 -e 10
>```
>
>启动64个线程,轰//炸多个人的手机号(198xxxxxxxx,199xxxxxxxx), 每次间隔30秒, 开启代理,每次轰炸在10个代理中随机选择一个代理搭配一个api
>
>```shell
>python smsboom.py run -t 64 -p 198xxxxxxxx -p 199xxxxxxxx -f 60 -i 30 -e 10
>```
>
>### 效果展现
>
>![](README.assets/test.gif)

### Flask 前端调试

> **前提是已经根据前文 Quick Start 的方式安装好 环境**

```shell
python run_flask_app.py start -p 9090 # 监听9090端口
```

**运行帮助:**
```shell
Usage: run_flask_app.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  init         初始化数据库
  json2sqlite  将json数据转为sqlite数据库
  sqlite2json  将sqlite数据转为json
  start        启动 flask app
```

```shell
Usage: run_flask_app.py start [OPTIONS]

  启动 flask app

Options:
  -h, --host TEXT     监听地址
  -p, --port INTEGER  监听端口
  --help              Show this message and exit.
```

默认监听 *0.0.0.0:9090* 地址,浏览器访问[http://127.0.0.1:9090/admin/](http://127.0.0.1:9090/admin/)若无意外,就可以出现前端调试界面。

![](img/webui-test.png)  
![](img/webui-test-2.png)  
