#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Package này dùng để mở rộng open edx app (dạng micro app)
"""
__apps__={}
__register_apps__ = {}
__controllers__=[]
def create(urlpatterns):
    """
    Tạp app
    :param name:
    :param host_dir:
    :return:
    """
    if isinstance(urlpatterns,tuple):
        from django.conf.urls import include, patterns, url
        import re
        for item in __controllers__:
            if not __apps__.has_key(item.instance.app_name):
                import os
                import path
                server_static_path = os.sep.join([
                    item.instance.app_dir,"static"
                ])
                urlpatterns+=(
                    url(r'^' + item.instance.host_dir + '/static/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': server_static_path, 'show_indexes': True}),
                )
                __apps__.update({
                    item.instance.app_name:item.instance.app_name
                })
            if item.url=="":
                urlpatterns +=(
                    url(r"^"+item.instance.host_dir +"$",item.instance.__view_exec__),
                    url(r"^"+item.instance.host_dir +"/$",item.instance.__view_exec__)
                )
            else:
                urlpatterns += (
                    url(r"^"+item.instance.host_dir +"/"+item.url+"$", item.instance.__view_exec__),
                    url(r"^"+item.instance.host_dir +"/"+item.url+"/$", item.instance.__view_exec__)
                )
        # urlpatterns += (
        #     url(r'config/self_paced', ConfigurationModelCurrentAPIView.as_view(model=SelfPacedConfiguration)),
        #     url(r'config/programs', ConfigurationModelCurrentAPIView.as_view(model=ProgramsApiConfig)),
        #     url(r'config/catalog', ConfigurationModelCurrentAPIView.as_view(model=CatalogIntegration)),
        #     url(r'config/forums', ConfigurationModelCurrentAPIView.as_view(model=ForumsConfig)),
        # )
    return urlpatterns
from . controllers import BaseController,Controller

def load_apps(path_to_app_dir,urlpatterns):
    import os
    import sys
    import imp
    def get_all_sub_dir():
        lst=os.walk(path_to_app_dir).next()[1]
        return lst
    lst_sub_dirs = get_all_sub_dir()
    for item in lst_sub_dirs:
        controller_dir = os.sep.join([path_to_app_dir,item,"controllers"])
        app_settings = imp.load_source("django.ext_apps.{0}.settings".format(item),os.sep.join([path_to_app_dir,item,"settings.py"]))
        sys.path.append(controller_dir)
        files = os.listdir(controller_dir)
        for file in files:
            controller_file = os.sep.join([controller_dir,file])
            m = imp.load_source("{0}.{1}".format(item,file.split('.')[0]),controller_file)
            controller_instance=__controllers__[__controllers__.__len__()-1].instance
            controller_instance.app_dir = path_to_app_dir

            """
            # self.controllerClass()
            if self.instance.app_name==None:
                raise Exception("{0} do not have 'app_name'".format(self.controllerClass))
            if self.instance.app_dir==None:
                raise Exception("{0} do not have 'app_dir'".format(self.controllerClass))
            """
            x=1
        print files



