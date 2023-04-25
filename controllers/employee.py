# -*- coding: utf-8 -*-
# try something like
from gluon.tools import Crud
crud = Crud(db)

def index(): 
    if len(request.args):
        page=int(request.args[0])
    else: 
        page=0
    items_per_page=10
    sel_emp=''
    limitby=(page*items_per_page, (page+1)*items_per_page+1)
    if request.vars.employee_id:
        print('No request')
        sel_emp=int(request.vars.employee_id)
        rows = db((db.auth_user.id==request.vars.employee_id)).select(db.auth_user.ALL,db.team.team_name,
                                    left=db.team.on(db.team.id == db.auth_user.team_id), limitby=limitby) 
    else:
        print('show all') 
        rows = db(db.auth_user).select(db.auth_user.ALL,db.team.team_name,
                                    left=db.team.on(db.team.id == db.auth_user.team_id), limitby=limitby) 
    # return db._lastsql
    employees=db(db.auth_user).select()
    print(employees)
    return dict(rows=rows, page=page, items_per_page=items_per_page,employees=employees,sel_emp=sel_emp)

def create():
    teams=db(db.team).select()
    rows=db(db.auth_user).select()
    return locals()

def edit():
    if request.args(0):
        print('Edit: ', )
        teams = db(db.team).select()
        item  = db(db.auth_user.id==request.args(0)).select().first()
        return dict(item=item,teams=teams)

def submit():
    # db.auth_user.insert(
    #     first_name=request.vars.first_name,
    #     last_name=request.vars.last_name,
    #     email=request.vars.email,
    #     password="pbkdf2(1000,20,sha512)$9f1517b9b1eb04c9$1d2049e96dff6943a61ca67ebc17452db4721025",#123456
    #     phone=request.vars.phone,
    #     date_of_birth=request.vars.date_of_birth,
    #     emp_type=request.vars.emp_type,
    #     company=request.vars.company,
    #     designation=request.vars.designation,
    #     address=request.vars.address,
    #     team_id=request.vars.team_id,
    #     department=request.vars.department,
    #     date_of_joining=request.vars.date_of_joining
    #     )
    redirect(URL('employee','index'))

def show():
    if request.args(0):
        item  = db(db.auth_user.id==request.args(0)).select().first()
        teams = db(db.team).select()
        team_name = 'Not Assigned'
        emp_type = item.emp_type
        for team in teams:                      
            if (item.team_id == team.id):
                team_name = team.team_name    
    return locals()

def delete():
    if request.args(0):
        session.flash = T("Deleted Information")
        db(db.auth_user.id == request.args(0)).delete()
    return dict(redirect(URL('employee', 'index')))