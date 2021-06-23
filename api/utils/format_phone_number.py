def format_phone_number(phone_number: str) -> str:
    if len(phone_number) == 10:
        try:
            int(phone_number) # make sure it's all numbers
            return f'({phone_number[:3]}) {phone_number[3:6]}-{phone_number[6:]}'
        except:
            pass
    return phone_number