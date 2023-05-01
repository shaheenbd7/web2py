# from urllib import response
import json

def getWorklogs():
    
    print('called getWorklogs')

    user_id = request.vars.user_id
    
    if user_id==None:
        response_data = {'Result': 'User Id Not found.'}
    else:
        sql ="SELECT au.first_name as efname,au.last_name as elname,au2.first_name as afname,au2.last_name as alname, wl.* FROM work_logs as wl LEFT JOIN auth_user as au on au.id=wl.employee_id LEFT JOIN auth_user as au2 on au2.id=wl.assigned_by where wl.employee_id='"+str(user_id)+"'"
        rows = db.executesql(sql, as_dict=True)
        if len(rows) == 0:
            response_data = {'Result': 'No Found.'}
        else:
            worklogRecordStr = rows[0]
            response_data={
                'First Name' : worklogRecordStr['efname'],
                'Last Name' : worklogRecordStr['elname'],
            }
    data=response.json(response_data)
    return data
