from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from watchlist import app, db
from watchlist.forms import HelloForm
from watchlist.util import Util
from watchlist.models import User, Movie,Message,Stock,Stockvo
from watchlist.zhangtingmodel import Zhangting

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('index'))

        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))

    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        user = User.query.first()
        user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))


@app.route('/sayhello', methods=['GET', 'POST'])
def sayhello():
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        message = Message(body=body, name=name)
        db.session.add(message)
        db.session.commit()
        flash('Your message have been sent to the world!')
        return redirect(url_for('sayhello'))

    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('sayhello.html', form=form, messages=messages)

@app.route('/stocks',methods=['get'])
@login_required
def stocks():
    stockvos = []
    stocks = Stock.query.order_by(Stock.timestamp.desc()).all()
    for m in stocks:
        itemcode= m.code
        itemppercent= Util.stock_data(itemcode)

        stockvo = Stockvo(id=m.id,name=m.name, code=m.code,uptimes=m.uptimes,percent=itemppercent,
                          lbc=0,
                          hs=0,
                          zj=0
                          )
    #stockvo = Stockvo(id=1,name='name', code='code',uptimes=1,percent='5%')

        stockvos.append(stockvo)

    return render_template('stocks.html',stockvos=stockvos)

@app.route('/zhangting',methods=['get'])
@login_required
def zhangting():
    # zhangtings= Zhangting.query.order_by(Zhangting.lbc.desc()).all()
    zhangtings= Zhangting.query.filter(Zhangting.lbc >1).order_by(Zhangting.lbc.desc(),Zhangting.zj.desc()).all()
    stockvos=[]
    for m in zhangtings:
        #print(Util.to_dict(m))
        itemcode = m.dm[2:8]
        # print(itemcode + '---' +m.dm)
        itemppercent = Util.stock_data(itemcode)

        stockvo = Stockvo(id=m.id, name=m.mc,
                          code=m.dm,
                          uptimes=m.lbc,
                          percent=itemppercent,
                          lbc = m.lbc,
                          hs = m.hs,
                          zj = '%.2f' % (int(m.zj) / 100000000) + '亿'
                          )
        stockvos.append(stockvo)
    return render_template('zhangting.html',stockvos=stockvos)





@app.route('/stocks/edit/<int:stock_id>', methods=['GET', 'POST'])
@login_required
def stock_edit(stock_id):
    stock = Stock.query.get_or_404(stock_id)

    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']

        if not name or not code or len(code) != 6 or len(name) > 60:
            flash('Invalid input.')
            return redirect(url_for('stock_edit', stock_id=stock_id))

        stock.name = name
        stock.code = code
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('stocks'))

    return render_template('stock-edit.html', stock=stock)


@app.route('/stocks/delete/<int:stock_id>', methods=['POST'])
@login_required
def stock_delete(stock_id):
    stock = Stock.query.get_or_404(stock_id)
    db.session.delete(stock)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('stocks'))