import phonenumbers
def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%']
    val = "correct"
    if len(passwd) < 6:
        val = 'Password length should be at least 6'
    if len(passwd) > 20:
        val = 'Password length should be not be greater than 15'
    if not any(char.isdigit() for char in passwd):
        val = 'Password should have at least one numeral'
    if not any(char.isupper() for char in passwd):
        val = 'Password should have at least one uppercase letter'
    if not any(char.islower() for char in passwd):
        val = 'Password should have at least one lowercase letter'
    if not any(char in SpecialSym for char in passwd):
        val = 'Password should have at least one of the symbols $@#'
    return val


def phone_verify(num):
    try:
        if num[0] == '+' and num[1] == '9' and num[2] == '1':
            my_number = phonenumbers.parse(num)
            pv = phonenumbers.is_valid_number(my_number)
        else:
            pv = False
    except Exception:
        pv= False
    return pv


