from utils import validate_key, validate_type

 
def validate_request_body(body, request_type):
        if request_type == 'POST':
                #validate key 
                validate_key(body, 'firstname')
                validate_key(body, 'lastname')
                validate_key(body, 'id')
                validate_key(body, 'profile')

                #validate types                
                validate_type(body, 'firstname', str)
                validate_type(body, 'lastname', str)
                validate_type(body, 'id', str)
                validate_type(body, 'profile', list)
        