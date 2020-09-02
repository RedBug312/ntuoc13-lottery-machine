from flask import Blueprint, render_template, url_for, request, abort, redirect
import random

from ..models import db


lottery = Blueprint('lottery', __name__)


@lottery.route('/lottery/draw/<role>')
def draw(role):
    prefixes = {'undergrad': 'B', 'grad': 'RD'}
    if role not in prefixes.keys():
        return abort(404)  # Invalid role found

    try:
        i = request.args.get('i', default=0, type=int)
        seed = request.args.get('seed', type=int)
    except ValueError:
        return abort(401)  # When argument failed casting
    if not seed:
        rand = random.randint(100000, 999999)
        return redirect(url_for('.draw', role=role, i=0, seed=rand))

    prefix = prefixes[role]
    winners = db.draw(n=3, seed=seed, prefix=prefix)
    if winners.empty:
        return abort(404)  # When no one can be drawn
    elif i >= winners.shape[0]:
        return redirect(url_for('.draw', role=role))

    link = url_for('.draw', role=role, i=(i + 1), seed=seed)
    name = winners.iloc[i].NAME
    desc = winners.iloc[i].STID
    return render_template('bingo.pug', link=link, name=name, desc=desc)


@lottery.route('/lottery/idle/<role>')
def idle(role):
    link = url_for('.draw', role=role)
    return render_template('bingo.pug', link=link)
