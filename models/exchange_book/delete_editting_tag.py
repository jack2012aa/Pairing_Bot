from models import database

def delete_editting_tag(userID: str, tag: str):
    '''Delete user's tag in editting_tag table'''

    cursor = database.cursor()
    cursor.execute(f"DELETE FROM editting_tags WHERE userID = '{userID}' AND tag = '{tag}';")
    database.commit()
    cursor.close()
    return 0