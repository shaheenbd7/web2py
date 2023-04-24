# -*- coding: utf-8 -*-
# try something like

# The first line import datetime imports the built-in Python datetime module, which provides classes for working with dates and times.

# The second line from gluon.tools import Crud imports the Crud class from the gluon.tools module. The Crud class is a tool provided by web2py to simplify the creation of Create-Read-Update-Delete (CRUD) interfaces for database tables.

# The third line crud = Crud(db) creates an instance of the Crud class, passing in the db object, which is a global object in web2py representing the application's database connection. This crud object can then be used to perform CRUD operations on the database tables, such as creating records, querying records, updating records, and deleting records.

# Overall, these lines are typically included in a web2py controller to set up the Crud tool and datetime module, which can be used in that controller's functions to interact with the database and work with dates and times.

import datetime
from gluon.tools import Crud
crud = Crud(db)

def index(): 
    # return dict(message="hello from worklog.py")

    if len(request.args): 
        page=int(request.args[0])
    else: 
        page=0
    items_per_page=10  
    condition=''
    sel_emp=''
    if request.vars.employee_id:
        print('int(request.vars.employee_id): ' , int(request.vars.employee_id))
        items_per_page=100
        sel_emp=int(request.vars.employee_id)
        condition+=" and wl.employee_id = '" + request.vars.employee_id + "'"
    limitby=(page*items_per_page, (page+1)*items_per_page+1)
    user_id=auth.user.id
    if auth.user.emp_type=="Admin":
        # sql =  "SELECT au.first_name as efname,au.last_name as elname,"
        # sql += "au2.first_name as afname,au2.last_name as alname, wl.* FROM work_logs"
        # sql += " as wl LEFT JOIN auth_user as au on au.id=wl.employee_id LEFT JOIN auth_user"
        # sql += " as au2 on au2.id=wl.assigned_by where 1 "+condition
        # sql += " limit "+str(limitby[0]) +","+str(limitby[1])
        
        # sql ="SELECT au.first_name as efname,au.last_name as elname,au2.first_name as afname"
        # sql += " , au2.last_name as alname, wl.* FROM work_logs as wl LEFT JOIN auth_user as au"
        # sql += " on au.id=wl.employee_id LEFT JOIN auth_user as au2 on au2.id=wl.assigned_by" 
        # sql += " where wl.employee_id="+str(user_id)
        sql ="SELECT au.first_name as efname,au.last_name as elname,au2.first_name as afname,au2.last_name as alname, wl.* FROM work_logs as wl LEFT JOIN auth_user as au on au.id=wl.employee_id LEFT JOIN auth_user as au2 on au2.id=wl.assigned_by"

    else:
        # sql ="SELECT au.first_name as efname,au.last_name as elname,au2.first_name as afname"
        # sql += ",au2.last_name as alname, wl.* FROM work_logs as wl LEFT JOIN auth_user as au"
        # sql += " on au.id=wl.employee_id LEFT JOIN auth_user as au2 on au2.id=wl.assigned_by" 
        # sql += " where wl.employee_id='"+str(user_id)
        sql ="SELECT au.first_name as efname,au.last_name as elname,au2.first_name as afname,au2.last_name as alname, wl.* FROM work_logs as wl LEFT JOIN auth_user as au on au.id=wl.employee_id LEFT JOIN auth_user as au2 on au2.id=wl.assigned_by where wl.employee_id='"+str(user_id)+"'"
        print('General User')
        print('user ID: ', user_id)
    # return sql
    rows = db.executesql(sql, as_dict=True)
    employees=db(db.auth_user).select()
    print(rows)
    return dict(rows=rows, page=page, items_per_page=items_per_page,employees=employees,sel_emp=sel_emp)

def create():
    teams=db(db.team).select()
    employees=db(db.auth_user).select()
    return locals()

def submit():
    db.work_logs.insert(
        employee_id=request.vars.employee_id,
        assigned_by=auth.user.id,
        task_type=request.vars.task_type,
        task_details=request.vars.task_details,
        feedback=request.vars.feedback,
        created_by=auth.user.id,
        updated_by=auth.user.id,
        team_id=request.vars.team_id
        )
    redirect(URL('worklog','index'))

def show():
    if request.args(0):
        teams=db(db.team).select()
        employees=db(db.auth_user).select()
        item = db(db.work_logs.id==request.args(0)).select().first()
    return locals()

def edit():
    if request.args(0):
        teams=db(db.teams).select()
        employees=db(db.auth_user).select()
        item = db(db.work_logs.id==request.args(0)).select().first()
        manage=db(db.auth_user.id==item.employee_id).select()
        return dict(item=item,teams=teams,employees=employees,manage=manage)


def update():
        work_log = db(db.work_logs.id == request.args(0)).select().first()
        work_log.update_record(
        tm_id=request.vars.tm_id,
        log_date=request.vars.log_date,
        assigned_by=request.vars.assigned_by,
        work_details=request.vars.work_details,
        play_details=request.vars.play_details,
        support_details=request.vars.support_details,
        note_details=request.vars.note_details,
        updated_by=auth.user.id,
        updated_at=datetime.date.today() 
        ) 
        redirect(URL('work_log','index'))

def delete():
    if request.args(0):
        session.flash = T("Deleted Information")
        db(db.work_logs.id == request.args(0)).delete()
    return dict(redirect(URL('work_log', 'index')))
def feedback():
    if request.args(0):
        teams=db(db.teams).select()
        employees=db(db.auth_user).select()
        item = db(db.work_logs.id==request.args(0)).select().first()
        manage=db(db.auth_user.id==item.employee_id).select()
        return dict(item=item,teams=teams,employees=employees,manage=manage)
def reply():
    work_log = db(db.work_logs.id == request.args(0)).select().first()
    work_log.update_record(
    feedback_details=request.vars.feedback_details,
    updated_by=auth.user.id,
    updated_at=datetime.date.today() 
    ) 
    redirect(URL('default','index'))