def is_cabinet_secretary(user):
    return user.is_authenticated and user.role == 'cabinet_secretary'

def is_county_director(user):
    return user.is_authenticated and user.role == 'county_director'

def is_subcounty_director(user):
    return user.is_authenticated and user.role == 'subcounty_director'

def is_school_admin(user):
    return user.is_authenticated and user.role == 'school_admin'

def is_teacher(user):
    return user.is_authenticated and user.role == 'teacher'
