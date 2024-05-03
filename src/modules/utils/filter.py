def filterFoundAccounts(site):
    if site["status"] == "FOUND":
        return True
    else:
        return False