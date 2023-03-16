def check_admin(claims):
    if not claims.get("is_admin", False):
        raise Exception("You do not have the required permissions")
