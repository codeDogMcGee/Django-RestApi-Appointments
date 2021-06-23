from django.core.exceptions import ValidationError

def validate(password):
    assert type(password) == str

    min_length = 8
    max_length = 30
    # special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '?']
    numbers = list(range(10))


    # test min and max length
    if len(password) < min_length:
        raise ValidationError('Password must be at least %(min_length)s characters.', params={'min_length': min_length})

    if len(password) > max_length:
        raise ValidationError('Password must be less than %(max_length)s characters.', params={'max_length': max_length})

    # # check for special characters
    # special_character_found = False
    # for _char in special_chars:
    #     if _char in password:
    #         special_character_found = True
    #         break
    
    # if special_character_found is False:
    #     raise ValidationError('Password must contain a special character %(special_chars)s', params={'special_chars': special_chars})
        
    # check for numbers
    number_found = False
    for num in numbers:
        if str(num) in password:
            number_found = True
            break
    
    if number_found is False:
        raise ValidationError('Password must contain a number %(numbers)s', params={'numbers': numbers})

    return password
