import os
from flask import render_template, jsonify, Blueprint, redirect, url_for, request
from sqlalchemy.sql.expression import union_all

from CTFd import utils
from CTFd.models import db, Teams, Solves, Awards, Challenges
from CTFd.plugins import register_plugin_asset
from CTFd.utils import override_template
from models import Classification, create_db

def load(app):
    create_db(app)
    dir_path = os.path.dirname(os.path.realpath(__file__))

    template_path = os.path.join(dir_path, 'scoreboard.html')
    override_template('scoreboard.html', open(template_path).read())

    register_plugin_asset(app, asset_path='/plugins/ctfd-classified-scoreboard-plugin/scoreboard.js')

    def get_standings(admin=False, count=None, classification=None):
        scores = db.session.query(
                    Solves.teamid.label('teamid'),
                    db.func.sum(Challenges.value).label('score'),
                    db.func.max(Solves.date).label('date')
                ).join(Challenges).group_by(Solves.teamid)

        awards = db.session.query(
                    Awards.teamid.label('teamid'),
                    db.func.sum(Awards.value).label('score'),
                    db.func.max(Awards.date).label('date')
                ).group_by(Awards.teamid)

        freeze = utils.get_config('freeze')
        if not admin and freeze:
            scores = scores.filter(Solves.date < utils.unix_time_to_utc(freeze))
            awards = awards.filter(Awards.date < utils.unix_time_to_utc(freeze))

        results = union_all(scores, awards).alias('results')

        sumscores = db.session.query(
                        results.columns.teamid,
                        db.func.sum(results.columns.score).label('score'),
                        db.func.max(results.columns.date).label('date')
                    ).group_by(results.columns.teamid).subquery()

        if admin:
            standings_query = db.session.query(
                                Teams.id.label('teamid'),
                                Teams.name.label('name'),
                                Teams.banned, sumscores.columns.score,
                                Classification.classification
                            )\
                            .join(sumscores, Teams.id == sumscores.columns.teamid) \
                            .join(Classification, Teams.id == Classification.id) \
                            .order_by(sumscores.columns.score.desc(), sumscores.columns.date)
        else:
            standings_query = db.session.query(
                                Teams.id.label('teamid'),
                                Teams.name.label('name'),
                                sumscores.columns.score,
                                Classification.classification
                            )\
                            .join(sumscores, Teams.id == sumscores.columns.teamid) \
                            .join(Classification, Teams.id == Classification.id) \
                            .filter(Teams.banned == False) \
                            .order_by(sumscores.columns.score.desc(), sumscores.columns.date)

        if classification and count:
            standings = standings_query.filter(Classification.classification == classification).limit(count).all()
    	elif classification:
            standings = standings_query.filter(Classification.classification == classification).all()
        elif count:
            standings = standings_query.limit(count).all()
        else:
            standings = standings_query.all()

        return standings

    def scoreboard_view():
        classifications = []
        for classification in db.session.query(Classification.classification).distinct():
            classifications.append(classification[0])
        db.session.close()

        classifications = sorted(classifications, reverse=True)

        if utils.get_config('view_scoreboard_if_authed') and not utils.authed():
            return redirect(url_for('auth.login', next=request.path))
        if utils.hide_scores():
            return render_template('scoreboard.html', errors=['Scores are currently hidden'])
        standings = get_standings()
        return render_template('scoreboard.html', teams=standings, score_frozen=utils.is_scoreboard_frozen(), classifications=classifications)

    def scores():
        json = {'standings': []}
        if utils.get_config('view_scoreboard_if_authed') and not utils.authed():
            return redirect(url_for('auth.login', next=request.path))
        if utils.hide_scores():
            return jsonify(json)

        standings = get_standings()

        for i, x in enumerate(standings):
            json['standings'].append({'pos': i + 1, 'id': x.teamid, 'team': x.name, 'score': int(x.score)})
        return jsonify(json)

    @app.route('/scores/<classification>')
    def classified_scores(classification):
        json = {'standings': []}
        if utils.get_config('view_scoreboard_if_authed') and not utils.authed():
            return redirect(url_for('auth.login', next=request.path))
        if utils.hide_scores():
            return jsonify(json)

        standings = get_standings(classification=classification)

        for i, x in enumerate(standings):
            json['standings'].append({'pos': i + 1, 'id': x.teamid, 'team': x.name, 'score': int(x.score)})
        return jsonify(json)

    @app.route('/top/<int:count>/<classification>')
    def classified_topteams(count, classification):
        json = {'places': {}}
        if utils.get_config('view_scoreboard_if_authed') and not utils.authed():
            return redirect(url_for('auth.login', next=request.path))
        if utils.hide_scores():
            return jsonify(json)

        if count > 20 or count < 0:
            count = 10

        standings = get_standings(count=count, classification=classification)

        team_ids = [team.teamid for team in standings]

        solves = Solves.query.filter(Solves.teamid.in_(team_ids))
        awards = Awards.query.filter(Awards.teamid.in_(team_ids))

        freeze = utils.get_config('freeze')

        if freeze:
            solves = solves.filter(Solves.date < utils.unix_time_to_utc(freeze))
            awards = awards.filter(Awards.date < utils.unix_time_to_utc(freeze))

        solves = solves.all()
        awards = awards.all()

        for i, team in enumerate(team_ids):
            json['places'][i + 1] = {
                'id': standings[i].teamid,
                'name': standings[i].name,
                'solves': []
            }
            for solve in solves:
                if solve.teamid == team:
                    json['places'][i + 1]['solves'].append({
                        'chal': solve.chalid,
                        'team': solve.teamid,
                        'value': solve.chal.value,
                        'time': utils.unix_time(solve.date)
                    })
            for award in awards:
                if award.teamid == team:
                    json['places'][i + 1]['solves'].append({
                        'chal': None,
                        'team': award.teamid,
                        'value': award.value,
                        'time': utils.unix_time(award.date)
                    })
            json['places'][i + 1]['solves'] = sorted(json['places'][i + 1]['solves'], key=lambda k: k['time'])

        return jsonify(json)
        
    app.view_functions['scoreboard.scoreboard_view'] = scoreboard_view
    app.view_functions['scoreboard.scores'] = scores
