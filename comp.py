
import unohelper

from com.sun.star.frame import XDispatchProvider, XDispatch, FeatureStateEvent
from com.sun.star.lang import XInitialization, XServiceInfo

class Dispatcher(unohelper.Base, XDispatch):
    
    def __init__(self, ctx, url, frame):
        self.ctx = ctx
        self.frame = frame
        self.url = url
        self.controls = {}
    
    def _notify(self, url, state, enabled=True):
        control = self.controls.get(url.Complete, None)
        if control:
            ev = FeatureStateEvent(self, url, "", enabled, False, state)
            control.statusChanged(ev)
    
    def set_state(self, checked):
        """ Set check state of the menu entry. """
        self._notify(self.url, checked)
    
    def switch_adjust_height(self, switch=True):
        """ Switches IsAdjustHeightEnabled state and returns new state. """
        try:
            model = self.frame.getController().getModel()
            status = model.IsAdjustHeightEnabled
            if switch:
                model.IsAdjustHeightEnabled = not status
                return model.IsAdjustHeightEnabled
            return status
        except:
            raise Exception()
    
    # XDispatch
    def dispatch(self, url, args):
        try:
            state = self.switch_adjust_height()
            self.set_state(state)
        except:
            pass
    
    def addStatusListener(self, control, url):
        self.controls[url.Complete] = control
        try:
            self.set_state(self.switch_adjust_height(False))
        except:
            pass
    
    def removeStatusListener(self, control, url):
        try:
            pass#self.controls.pop(url.Complete)
        except:
            pass


class ProtocolHandler(unohelper.Base, XDispatchProvider, XInitialization, XServiceInfo):
    
    IMPLE_NAME = "mytools.calc.AdjustHeight"
    SERVICE_NAMES = IMPLE_NAME, "com.sun.star.frame.ProtocolHandler"
    
    # XServiceInfo
    def supportsService(self,name):
        return name in self.__class__.SERVICE_NAMES
    
    def getImplementationName(self):
        return self.__class__.IMPLE_NAME
    
    def getSupportedServiceNames(self):
        return self.__class__.SERVICE_NAMES
    
    @classmethod
    def get_info(klass):
        return klass, klass.IMPLE_NAME, klass.SERVICE_NAMES
    
    def __init__(self, ctx, *args):
        self.ctx = ctx
        self.frame = None
        self.initialize(args)
    
    # XInitialization
    def initialize(self, args):
        if len(args) > 0:
            self.frame = args[0]
    
    # XDispatchProvider
    def queryDispatch(self, url, name, flag):
        if url.Complete == "mytools.calc.AdjustHeight:Adjust" and \
           self.check_document_type(self.frame, ("com.sun.star.sheet.SpreadsheetDocument",)):
            return Dispatcher(self.ctx, url, self.frame)
        return None
    
    def queryDispatches(self, descs):
        return tuple(
            [self.queryDispatch(desc.FeatureURL, desc.FrameName, desc.SearchFlags) 
                for desc in descs])
    
    def check_document_type(self, doc, doc_types):
        """ Checks passed document type is one of doc_types. """
        try:
            return self.ctx.getServiceManager().createInstanceWithContext(
                "com.sun.star.frame.ModuleManager", self.ctx).identify(doc) in doc_types
        except:
            return False


g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
    *ProtocolHandler.get_info())
