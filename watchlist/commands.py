import datetime

import click
import json
import demjson

from sqlalchemy import func

from watchlist import app, db
from watchlist.models import User, Movie, Stock,Config
from watchlist.zhangtingmodel import Zhangting
from watchlist.util import Util


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')

@app.cli.command()
@click.option('--name', prompt=True, help='The name of config.')
@click.option('--value', prompt=True, help='The value of config.')
def addconfig(name, value):
    """Create Table."""
    db.create_all()

    config = Config.query.filter(Config.name==name).first()
    if config is not None:
        click.echo('Updating config...')
        config.name = name
        config.value = value
    else:
        click.echo('Creating config...')
        config = Config(name=name, value=value)
        config.name = name
        config.value = value
        db.session.add(config)

    db.session.commit()
    click.echo('Done.')
@app.cli.command()
def getconfig():
    config = Config.query.filter(Config.name == 'license').first()

    click.echo('Done.==' +config.value)


@app.cli.command()
def initstock():
    """Create Table Stock."""
    db.create_all()
    """Mock Data."""
    stocks = [
        {'name': '宝馨科技', 'code': '002514', 'uptimes':0},
        {'name': '传艺科技', 'code': '002866', 'uptimes':0},

    ]
    for m in stocks:
        stockItem = Stock(name=m['name'], code=m['code'],uptimes=m['uptimes'])
        db.session.add(stockItem)

    db.session.commit()
    click.echo('Done.')

#T增加涨停数据初始化的命令，调用工具类
@app.cli.command()
def zhangting():
    date_now = datetime.datetime.now()
    date_str=str(date_now.strftime("%Y-%m-%d"))
    result=Util.zhangting_data(date_str);
    #click.echo(result)
    #stocks = Zhangting.query.order_by(Zhangting.zj.desc()).all()
    click.echo('Done.' +result)

@app.cli.command()
def datest():
    #查询连板数量，按最高到低分组展现连板股次日竞价的表现
    lbsl=db.session.query(Zhangting.lbc).group_by(Zhangting.lbc).order_by(Zhangting.lbc.desc()).all()
    #print(lbsl)
    for m in lbsl:
        print(int(m[0]))
    click.echo('Done.' )

@app.cli.command()
def d2():
    #查询连板数量，按最高到低分组展现连板股次日竞价的表现
    lbsl=getlbcstocks(3)
    #print(lbsl)
    for m in lbsl:
        item=Util.to_dict(m)
        print(item)
    click.echo('Done.')





@app.cli.command()
def datetimetest():
    date_str = datetime.datetime.now()
    #获取昨天
    date_str_yesday=datetime.date.today()-datetime.timedelta(days=1)
    click.echo('Done.'+ str(date_str_yesday.strftime("%Y-%m-%d")))


def getlbcstocks(lbc):
    lbsl = Zhangting.query.filter(Zhangting.lbc == lbc).order_by(Zhangting.zj.desc()).all()

    return lbsl