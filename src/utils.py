def check_req_data(req : dict , required) :
    if len(req.keys()) != len(required) : 
        return False
    for i in req.keys():
        if i not in required :
            return False
    return True

