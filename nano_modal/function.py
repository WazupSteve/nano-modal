class Function:
    def __init__(self,func):
        self.func = func

    def local(self,*args,**kwargs):
        return self.func(*args,**kwargs)

    def __call__(self,*args,**kwargs):
        return self.local(*args,**kwargs)

    def remote(self,*args,**kwargs):
        #stub
        pass