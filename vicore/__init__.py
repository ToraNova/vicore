'''
this the shared class for viauth, vicms and vimail.
'''

from flask import redirect, url_for, flash, Blueprint
from collections import namedtuple

AppArch = namedtuple('AppArch', ['bp'])
AppArchExt = namedtuple('AppArchExt', ['bp','ext'])

class BaseArch:
    # for vicms, where reference 'content' is always needed
    def _cms_reroute(self, fromkey):
        if self._rkarg.get(fromkey):
            return redirect(url_for(self._route[fromkey], content=self._viname, **self._rkarg.get(fromkey)))
        else:
            return redirect(url_for(self._route[fromkey], content=self._viname))

    # the basic reroute function
    def _reroute(self, fromkey):
        if self._rkarg.get(fromkey):
            return redirect(url_for(self._route[fromkey], **self._rkarg.get(fromkey)))
        else:
            return redirect(url_for(self._route[fromkey]))

    def _default_tp(self, key, value):
        if not self._templ.get(key):
            self._templ[key] = value

    def _default_rt(self, key, value):
        if not self._route.get(key):
            self._route[key] = value

    # initializes a blueprint with url prefixing
    def _init_bp(self):
        return Blueprint(self._viname, __name__, url_prefix = self._urlprefix)

    def set_callback(self, event, cbfunc):
        if not callable(cbfunc):
            raise TypeError("callback function should be callable")
        self._callbacks[event] = cbfunc

    def callback(self, event, *args):
        return self._callbacks[event](*args)

    # convenience functions
    def error(self, msg):
        self.callback('err', msg)

    def ok(self, msg):
        self.callback('ok', msg)

    def warn(self, msg):
        self.callback('warn', msg)

    def ex(self, e):
        self.callback('ex', e)

    def __init__(self, viname, templates = {}, reroutes = {}, reroutes_kwarg = {}, url_prefix = None):
        self._templ = templates
        self._route = reroutes
        self._rkarg = reroutes_kwarg
        if url_prefix is None:
            self._urlprefix = '/%s' % viname
        elif url_prefix == '/':
            self._urlprefix = None
        else:
            self._urlprefix = url_prefix
        self._viname = viname

        self._callbacks = {
                'err': lambda msg : flash(msg, 'err'),
                'ok': lambda msg : flash(msg, 'ok'),
                'warn': lambda msg : flash(msg, 'warn'),
                'ex': lambda ex : flash("an exception (%s) has occurred: %s" % (type(ex).__name__, str(ex)), 'err'),
        }
