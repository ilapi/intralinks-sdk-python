EXCHANGE_MAX_NAME_LENGTH = 100
EXCHANGE_MAX_DESCRIPTION_LENGTH = 1000

FOLDER_FORBIDDEN_CHARS = {'/', '\\', ':', '*', '"', '<', '>', '?', '|'}
FOLDER_MAX_NAME_LENGTH = 60

def validate_folder(folder):
    if 'name' not in folder:
        raise Exception('No name')
    
    for c in VALIDATE_FOLDER_FORBIDDEN_CHARS:
        if c in folder['name']:
            raise Exception('Not allowed in name: {}'.format(c)) 
    
    if len(folder['name']) > VALIDATE_FOLDER_MAX_NAME_LENGTH:
        raise Exception('Exceed 60 characters: {}'.format(len(folder['name']))) 

GROUP_MAX_NAME_LENGTH = 49
GROUP_MAX_NOTE_LENGTH = 200
GROUP_MAX_ENTITY_COUNT_DELETE = 100