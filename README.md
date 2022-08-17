# Watchlist

Example application for flask tutorial "[Flask 入门教程](https://helloflask.com/book/3)".

Demo: http://watchlist.helloflask.com

![Screenshot](https://helloflask.com/screenshots/watchlist.png)


## Installation

clone:
```
$ git clone https://github.com/helloflask/watchlist.git
$ cd watchlist
```
create & active virtual enviroment then install dependencies:
```
$ python3 -m venv env  # use `python ...` on Windows  python -m venv env
$ source env/bin/activate  # use `env\Scripts\activate` on Windows
(env) $ pip install -r requirements.txt
```

generate fake data then run:
```
(env) $ flask forge
(env) $ flask run
* Running on http://127.0.0.1:5000/
```
```
使用 click.option() 装饰器设置的两个选项分别用来接受输入用户名和密码。执行 flask admin 命令，输入用户名和密码后，即可创建管理员账户。如果执行这个命令时账户已存在，则更新相关信息：

(env) $ flask admin
Username: greyli
Password: 123  # hide_input=True 会让密码输入隐藏
Repeat for confirmation: 123  # confirmation_prompt=True 会要求二次确认输入
Updating user...
Done.
```

## License

This project is licensed under the MIT License (see the
[LICENSE](LICENSE) file for details).
