from models import database
from flask import current_app
from datetime import datetime

def has_accept_invitation(userID: str):
    '''Whether user has an today-accepted invitation.'''

    sql = f"SELECT * FROM invitations WHERE (invitedID = '{userID}' OR invitorID = '{userID}') AND accept = 'T' AND DATE(checked_time) = current_date;"
    cursor = database.cursor()
    try:
        cursor.execute(sql)
        result = len(cursor.fetchall()) == 1
        cursor.close()
        #current_app.logger.debug(f"[{datetime.now()}] Call: has_accept_invitation({userID}), sql = {sql}, result = {result}")
        return result
    except:
        #current_app.logger.error(f"[{datetime.now()}] SQL error. Call: has_accept_invitation({userID}), sql = {sql}")
        cursor.close()
        return False