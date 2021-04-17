'''
this the shared class for viauth, vicms and vimail.
'''

from flask import redirect, url_for, flash, Blueprint
from collections import namedtuple

AppArch = namedtuple('AppArch', ['bp'])
AppArchExt = namedtuple('AppArchExt', ['bp','ext'])

class BaseArch:
    # default functions for vial project dev
    def _default_tp(self, route_name, default):
        if not self._templ.get(route_name):
            self._templ[route_name] = default

    def _default_rt(self, route_name, default):
        if not self._route.get(route_name):
            self._route[route_name] = default

    def _default_fm(self, route_name, default):
        if not self._flash.get(route_name):
            self._route[route_name] = default

    # for vicms, where reference 'content' is always needed
    # deprecated, kept for backward compatibility,
    # use _reroute_mod instead
    # use: call _reroute_mod('name', 'value') after reroute settings
    # to always insert url_for(... , name = value , ...) in reroute calls
    def _reroute_mod(self, farg_name, farg_value):
        for k in self._route.keys():
            if self._rkarg.get(k) is None:
                self._rkarg[k] = {farg_name: farg_value}
            else:
                self._rkarg[k][farg_name] = farg_value

    # the basic reroute function
    def _reroute(self, fromkey, **kwargs):
        if type(self._rkarg.get(fromkey)) is dict:
            passd = {}
            for k, v in self._rkarg.get(fromkey).items():
                if v is None and k in kwargs:
                    passd[k] = kwargs[k]
                else:
                    passd[k] = v
            return redirect(url_for(self._route[fromkey], **passd))
        return redirect(url_for(self._route[fromkey]))

    # initializes a blueprint with url prefixing
    def _init_bp(self):
        return Blueprint(self._viname, __name__, url_prefix = self._urlprefix)

    def rxcall(self, route, result, *args, **kwargs):
        if self._rxcall.get(route) is None or self._rxcall[route].get(result) is None:
            # unset, flash the first arg as msg
            if len(args) > 0:
                if type(args[0]) is str:
                    flash(args[0], result)
                elif isinstance(args[0], Exception):
                    flash('an exception (%s) has occurred: %s' % (type(args[0]).__name__, str(args[0])), 'err')
                else:
                    flash(str(args[0]), result)
            else:
                flash(route, result)
        else:
            # execute the callback
            self._rxcall[route][result](*args, **kwargs)

    # convenience functions
    def ok(self, route, *args, **kwargs):
        # all good
        self.rxcall(route,'ok',*args, **kwargs)

    def err(self, route, *args, **kwargs):
        # error caused by user
        self.rxcall(route,'err',*args, **kwargs)

    def ex(self, route, *args, **kwargs):
        # error caused by devs
        self.rxcall(route,'ex',*args, **kwargs)

    def warn(self,route, *args, **kwargs):
        # a warning
        self.rxcall(route, 'warn', *args, **kwargs)

    # viname - name of the vial
    # templates - the template dictionary, same for reroutes
    # reroutes_kwarg - additional kwarg to pass in during a reroute fcall
    # rex_callback - route execution callback, a function table at the end of a route execution
    # url_prefix - url prefix of a blueprint generated. use / to have NO prefix, leave it at None to default to /viname
    def __init__(self, viname, templates = {}, reroutes = {}, reroutes_kwarg = {}, rex_callback = {}, url_prefix = None):
        assert type(viname) is str
        assert type(templates) is dict
        assert type(reroutes) is dict
        assert type(reroutes_kwarg) is dict
        assert type(rex_callback) is dict
        assert type(url_prefix) is str or url_prefix is None
        self._templ = templates.copy()
        self._route = reroutes.copy()
        self._rkarg = reroutes_kwarg.copy()
        self._rxcall = rex_callback.copy()

        if url_prefix is None:
            self._urlprefix = '/%s' % viname
        elif url_prefix == '/':
            self._urlprefix = None
        else:
            self._urlprefix = url_prefix
        self._viname = viname
