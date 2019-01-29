import os
from flask import render_template, jsonify, Blueprint, redirect, url_for, request
from sqlalchemy.sql.expression import union_all

from CTFd import utils
from CTFd.models import db, Teams, Solves, Awards, Challenges
from CTFd.plugins import register_plugin_asset
from CTFd.utils import override_template

# -=- For TAMUctf, but can be left in without any problems -=-   
try:
    from CTFd.plugins.register.__init__ import tamu_test
except ImportError:
    print "\n-=-=-=-=-=-=-=-=-=-=-=-\
           \n\nAuto-Register Application not installed.\
           \n\n-=-=-=-=-=-=-=-=-=-=-=-\n"
# -=-

from sqlalchemy import ForeignKey
from CTFd.models import db
import re
import requests
from HTMLParser import HTMLParser
import logging
import os
import re
import time


from flask import current_app as app, render_template, request, redirect, url_for, session, Blueprint
from itsdangerous import TimedSerializer, BadTimeSignature, Signer, BadSignature
from passlib.hash import bcrypt_sha256
from sqlalchemy import ForeignKey
from werkzeug.routing import Rule

from CTFd import utils
from CTFd.models import db, Teams
from CTFd.plugins import register_plugin_assets_directory


import datetime
import hashlib
import json
from socket import inet_aton, inet_ntoa
from struct import unpack, pack, error as struct_error
from flask import current_app as app, render_template, request, redirect, jsonify, url_for, Blueprint, session
from passlib.hash import bcrypt_sha256
from sqlalchemy.sql import not_,or_
from CTFd.models import db, Teams, Solves, Awards, Challenges, WrongKeys, Keys, Tags, Files, Tracking, Pages, Config, Unlocks, DatabaseError, Hints, Unlocks
from CTFd.plugins.challenges import get_chal_class

from sqlalchemy.sql import or_

from CTFd.utils import ctftime, view_after_ctf, authed, unix_time, get_kpm, user_can_view_challenges, is_admin, get_config, get_ip, is_verified, ctf_started, ctf_ended, ctf_name, admins_only
# from CTFd.models import Hint
from CTFd.admin import admin
from CTFd.challenges import challenges
from CTFd.scoreboard import scoreboard, scores, get_standings

from flask_sqlalchemy import SQLAlchemy
from passlib.hash import bcrypt_sha256
from sqlalchemy.exc import DatabaseError
from sqlalchemy import String
from CTFd.plugins import register_plugin_asset
from CTFd import utils

from CTFd.plugins.challenges import get_chal_class

#-----------Global, set to what you need----------
initialBrackets = []
initialClassifications = []
#---------------------------------------

#-=-=-=-=-=-Classes-=-=-=-=-=-
class Classification(db.Model):
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, ForeignKey('teams.id'), primary_key=True)
    teamid = db.Column(db.Integer)
    classification = db.Column(db.String(128))
    other = db.Column(db.Integer)

    def __init__(self,id, classification):
        self.id = id
        self.teamid = id
        self.classification = classification

    def add_other(self, other):
        self.other = other

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

class Bracket(db.Model):
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    bracketid = db.Column(db.String(128))
    parentbracketid = db.Column(db.Integer)
    classification = db.Column(db.String(128))
    isparent = db.Column(db.Boolean)

    # add child argument here
    def __init__(self, bracketName, classificationName):
        self.bracketid = bracketName
        self.classification = classificationName

def load(app):
    app.db.create_all()

    classification = Blueprint('classification', __name__, template_folder='./')
               
    dir_path = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(dir_path, 'scoreboard.html')
    override_template('scoreboard.html', open(template_path).read())

    # register_plugin_assets_directory(app, base_path='/plugins/classification/static/')
    register_plugin_asset(app, asset_path='/plugins/classification/static/config.js')
    register_plugin_asset(app, asset_path='/plugins/classification/static/config.css')

    # Server side Configuration menu, honestly that post clasifeid should be made into a function
    @classification.route('/admin/plugins/classification', methods=['GET', 'POST'])
    @utils.admins_only
    def classified():
        if request.method == 'POST':
            teamid = request.form['id']
            previous = Classification.query.filter_by(id=teamid)
            for x in previous:
                db.session.delete(x)

            errors = []
            classification = request.form['classification']

            if classification == 'other':
                classification = request.form['new_classification']
            

            classify = Classification(int(teamid), classification)
            db.session.add(classify)
            db.session.commit()
            db.session.close()

        if request.method == 'GET' or request.method == 'POST':
            classifications = Classification.query.all()
            
            teams=[]
            scoring_teams=[]
            brackets=[]
            standings = get_standings()
            # Competitors with a score
            for i, x in enumerate(standings):
                pushed = 0
                for classification in classifications:
                    if classification.teamid == x.teamid:
                        teams.append({'id': x.teamid, 'name': x.name, 'class': classification.classification , 'score': x.score})
                        pushed = 1
                        break
                scoring_teams.append(x.teamid)
                if(pushed == 0):
                    teams.append({'id': x.teamid, 'name': x.name, 'class': '' , 'score': x.score})
            
            # Competitors with/without a score (limited to only without a score)
            for team in db.session.query(Teams.name, Teams.id, Teams.admin).all():
                if(team.admin == False):
                    pushed = 0
                    for classification in classifications:
                        if classification.teamid == team.id:
                            if(team.id not in scoring_teams):
                                teams.append({'id': team.id, 'name': team.name, 'class': classification.classification , 'score': ''})
                                pushed = 1
                    if(pushed == 0 and (team.id not in scoring_teams)):
                        teams.append({'id': team.id, 'name': team.name, 'class': '' , 'score': ''})
            
            classf=[]
            for clas in classifications:
                classf.append(clas.classification)
            classf=list(sorted(set(classf)))

# can/should be made into function

            if Bracket.query.first() is None:
                for x, y in zip(initialBrackets, initialClassifications):
                    new_bracket = Bracket(x, y)
                    db.session.add(new_bracket)
                db.session.commit()
            existingBrackets = Bracket.query.all()
            for x in existingBrackets:
                brackets.append({'id': x.id, 'name': x.bracketid, 'class': x.classification, 'parent': x.parentbracketid, 'isparent': x.isparent})
 #--           
            db.session.close()
        #print("Classifications: ", brackets)
        return render_template('config.html', teams=teams, classifications=classf, brackets=brackets )

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
            allBrackets = []
            classificationsLeft = []

            c=Classification
            allBrackets.append(classification)
            classificationsLeft.append(classification)
            while True:
                if len(classificationsLeft) > 0:
                    parentBracket = Bracket.query.filter_by(bracketid=classificationsLeft.pop())
                    for p in parentBracket:
                        child = Bracket.query.filter_by(parentbracketid=p.id)
                        for nested in child:
                            allBrackets.append(nested.bracketid)
                else:
                    standings = standings_query.filter(c.classification.in_(allBrackets)).limit(count).all()
                    break    


        elif classification:
            allBrackets = []
            classificationsLeft = []

            c=Classification
            allBrackets.append(classification)
            classificationsLeft.append(classification)
            while True:
                if len(classificationsLeft) > 0:
                    parentBracket = Bracket.query.filter_by(bracketid=classificationsLeft.pop())
                    for p in parentBracket:
                        child = Bracket.query.filter_by(parentbracketid=p.id)
                        for nested in child:
                            allBrackets.append(nested.bracketid)
                else:
                    standings = standings_query.filter(c.classification.in_(allBrackets)).all()
                    break

        else:
            print("KNOWKNWOKNWOKWNOKN")
            standings = standings_query.all()
        return standings

    def scoreboard_view():
        classifications = []
        brackets = []
        for classification in db.session.query(Classification.classification).distinct():
            classifications.append(classification[0])
        db.session.close()

        classifications = sorted(classifications, reverse=True)
        
        if Bracket.query.first() is None:
            for x, y in zip(initialBrackets, initialClassifications):
                new_bracket = Bracket(x, y)
                db.session.add(new_bracket)
                db.session.commit()
        existingBrackets = Bracket.query.all()
        for x in existingBrackets:
            brackets.append({'id': x.id, 'name': x.bracketid, 'class': x.classification, 'parent': x.parentbracketid, 'isparent': x.isparent})

        try:
          current_user_class = Classification.query.filter_by(id=session.get('id')).first().classification
        except:
          current_user_class = "ALL"
        try:
          current_user_other = Classification.query.filter_by(id=session.get('id')).first().other
        except:
          current_user_other = 0

        if utils.get_config('view_scoreboard_if_authed') and not utils.authed():
            return redirect(url_for('auth.login', next=request.path))
        if utils.hide_scores():
            return render_template('scoreboard.html', errors=['Scores are currently hidden'])
        standings = get_standings()
        print("Standings: ", standings)
        print("Classifications: ", classifications)
        print("Brackets: ", brackets)
        return render_template('scoreboard.html', teams=standings, score_frozen=utils.is_scoreboard_frozen(), classifications=classifications, brackets=brackets, current_user_class=current_user_class, current_user_other=current_user_other)

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

    def emptyBrackets():
        if Bracket.query.first() is None:
            brackets = initialBrackets
            for x, y in zip(initialBrackets, initialClassifications):
                new_bracket = Bracket(x, y)
                db.session.add(new_bracket)
            db.session.commit()

    def addParentBracket(child, parent):
        if child:
            childBracket = Bracket.query.filter_by(id=child).one()
            childBracket.parentbracketid = parent
            childBracket.isparent = None
            db.session.commit()

    def deleteAllChildren(parent):
        childBracket = Bracket.query.filter_by(parentbracketid=int(parent))
        for x in childBracket:
            x.parentbracketid = None
            x.isparent = True
        db.session.commit()

    @classification.route('/admin/plugins/classification/create', methods=['POST'])
    @utils.admins_only
    def create_bracket():
        if request.method == 'POST':
            new_bracket = request.form['new_bracket']
            create_classification = request.form['create_classification']
            child = request.form['childId']
            bracket = Bracket(new_bracket, create_classification)
            db.session.add(bracket)
            db.session.commit()
            addParentBracket(child, bracket.id)
            bracket.isparent = True
            db.session.close()
        return redirect('/admin/plugins/classification')

    @classification.route('/admin/plugins/classification/delete', methods=['POST'])
    @utils.admins_only
    def delete_bracket():
        if request.method == 'POST':
            d_bracket = request.form['submitDelete']
            bracket = Bracket.query.filter_by(id=d_bracket).one()
            deleteAllChildren(d_bracket)
            db.session.delete(bracket)
            db.session.commit()
            db.session.close()
            emptyBrackets()
        return redirect('/admin/plugins/classification')

    @classification.route('/admin/plugins/classification/edit', methods=['POST'])
    @utils.admins_only
    def edit_bracket():
        if request.method == 'POST':
            new_name = request.form['bracket_name']
            e_bracket = request.form['editId']
            child = request.form['childId']
            bracket = Bracket.query.filter_by(id=e_bracket).one()
            if bracket.bracketid is not new_name:
                bracket.bracketid = new_name
                db.session.commit()
            if child:
                print("e_bracket: ", e_bracket)
                print("child: ", child)
                print("bracket.parentbracketid: ", dir(bracket))
                if bracket.parentbracketid is None or ((int(e_bracket) is not int(child)) and (int(child) is not int(bracket.parentbracketid))):
                    addParentBracket(child, e_bracket)
            db.session.close()
        return redirect('/admin/plugins/classification')


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

    app.register_blueprint(classification)


    
