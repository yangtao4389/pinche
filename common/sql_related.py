import datetime
import decimal

def exe_sql(sql):
    from django.db import connection
    # connection = connections["statistic"]
    cr = connection.cursor()
    cr.execute(sql)
    try:
        connection.commit()
    except:
        pass
    return cr

def getmodelfield(modelobj):
    '''
    根据模型类获取对应的field与verbose_name
    :param modelobj:
    :return:
    '''
    fielddic={}
    for field in modelobj._meta.fields:
        fielddic[field.name] = field.verbose_name
    return fielddic

def render_rows(rows):
    ret = []
    for row in rows:
        tmp_row = {}
        for k,v in row.items():
            if type(v) == datetime.datetime:
                v = v.strftime("%Y-%m-%d %H:%M:%S")
            if type(v) == datetime.date:
                v = v.strftime("%Y-%m-%d")
            if type(v) == decimal.Decimal:
                v = float(v)
            tmp_row[k] = v
        ret.append(tmp_row)
    return ret