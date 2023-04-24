# -*- coding: utf-8 -*-
# try something like
def index(): 
    if not request.args(0):
        rows = db(db.team).select()
        return dict(rows=rows);
    else:
        rows = db(db.team.id.startswith(request.args(0))).select()
        return dict(rows=rows)

def create():
    rows=db(db.team).select()
    return locals()

def submit():
    db.team.insert(team_name=request.vars.team_name,
                    created_by=auth.user.id,
                    updated_by=auth.user.id)
    redirect(URL('team','index'))


def show():
    if request.args(0):
        item = db(db.team.id==request.args(0)).select().first()
    return locals()

def edit():
    if request.args(0):

        item = db(db.team.id==request.args(0)).select().first()
        return dict(item=item)

def update():
        team = db(db.team.id == request.args(0)).select().first()
        team.update_record(team_name=request.vars.team_name,
                            updated_by=auth.user.id,
                            updated_at=datetime.date.today()) 
        redirect(URL('team','index'))

def delete():
    if request.args(0):
        session.flash = T("Deleted Information")
        db(db.teams.id == request.args(0)).delete()
    return dict(redirect(URL('team', 'index')))