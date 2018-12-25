#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Model(object):
    def __init__(self):
        self.request=None
        self.response=None
class __controller_wrapper__(object):
    """
    Controllwer wrapper class
    """
    def __init__(self,*args,**kwargs):
        self.url=kwargs["url"]
        self.template=kwargs["template"]
        self.controllerClass=None

    def wrapper(self,*args,**kwargs):
        import xdj
        if issubclass(args[0],BaseController):
            self.controllerClass=args[0]
            self.instance =BaseController.__new__(self.controllerClass)
            super(self.controllerClass, self.instance).__init__()
            self.instance.url=self.url
            self.instance.template = self.template

            xdj.__controllers__.append(self)
        else:
            raise Exception("{0} mus be inherit from {1}".format(self.controllerClass,BaseController))


def Controller(*args,**kwargs):
    ret = __controller_wrapper__(*args,**kwargs)
    return ret.wrapper
class BaseController(object):
    def __init__(self):
        self.app_name=None
        self.app_dir=None
        self.url=None
        self.template=None
    def init_from_file_path(self,filePath):
        """
        Hàm này khởi tạo đường dẫn cho app
        :param filePath:
        :return:
        """
        import os
        self.app_dir= os.path.dirname(os.path.dirname(filePath))
        """
        Thực tế là chỉ cần lấy thư mục cha của thư mục cha của file
        """
    def __view_exec__(self,request):
        model=Model();
        model.request=request

        if request.method == 'GET':
            return self.on_get(model)
        if request.method == 'POST':
            return self.on_post(model)
    def render(self,model):
        from django.http import HttpResponse
        import os
        import sys
        from mako.template import Template
        from mako.lookup import TemplateLookup
        viewpath=os.sep.join([self.app_dir,"views"])

        ret_res = None
        mylookup = TemplateLookup(directories=[viewpath],
                                  default_filters=['decode.utf8'],
                                  input_encoding='utf-8',
                                  output_encoding='utf-8',
                                  encoding_errors='replace',

                                  )
        ret_res = mylookup.get_template(self.template).render(**model)
        return HttpResponse(ret_res)

