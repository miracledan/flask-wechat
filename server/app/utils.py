# -*- coding: utf-8 -*-

def safe_model_to_json(model):
    return model and model.to_json()
    
def singleton(cls, *args, **kw):  
    instances = {}  
    def _singleton():  
        if cls not in instances:  
            instances[cls] = cls(*args, **kw)  
        return instances[cls]  
    return _singleton 