from models import database
from flask import current_app
from datetime import datetime

def accept_invitation(invitorID:str, invitor_upload_time: str, invitedID: str, invited_upload_time: str):
    '''Accept invitation and expire all other invitations'''

    try:
        cursor = database.cursor()
        #Set accept and checked_time
        cursor.execute(f"UPDATE invitations SET accept = 'T', expired = 'T', checked_time = CURRENT_TIMESTAMP WHERE invitorID = '{invitorID}' AND invitedID = '{invitedID}' AND invited_upload_time = '{invited_upload_time}' AND invitor_upload_time = '{invitor_upload_time}';")

        #Insert into revert list
        cursor.execute(f"INSERT INTO revert_invitations_list (invitorID, invitor_upload_time, invitedID, invited_upload_time) SELECT invitorID, invitor_upload_time, invitedID, invited_upload_time FROM invitations WHERE (invitorID = '{invitorID}' OR invitedID = '{invitedID}' OR invitorID = '{invitedID}' OR invitedID = '{invitorID}') AND accept = 'F' AND deny = 'F' AND expired = 'F';")
        cursor.execute(f"INSERT INTO revert_books_list (userID, upload_time) SELECT userID, upload_time FROM books WHERE (userID = '{invitorID}' AND upload_time = '{invitor_upload_time}') OR (userID = '{invitedID}' AND upload_time = '{invited_upload_time}');")

        #Set expired/blocked
        cursor.execute(f"UPDATE invitations SET expired = 'T', checked_time = CURRENT_TIMESTAMP WHERE (invitorID = '{invitorID}' OR invitedID = '{invitedID}' OR invitorID = '{invitedID}' OR invitedID = '{invitorID}') AND accept = 'F' AND deny = 'F' AND expired = 'F';")
        cursor.execute(f"UPDATE books SET blocked = 'T' WHERE userID = '{invitorID}' AND upload_time = '{invitor_upload_time}';")
        cursor.execute(f"UPDATE books SET blocked = 'T' WHERE userID = '{invitedID}' AND upload_time = '{invited_upload_time}';")
        database.commit()
        cursor.close()
        
        return True
    except Exception as err:
        
        cursor.close()
        return False