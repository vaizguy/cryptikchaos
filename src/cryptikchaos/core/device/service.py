'''
Created on Jul 20, 2014

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

import os.path
from kivy import Logger

from plyer import uniqueid
from plyer import vibrator
from plyer import notification

from cryptikchaos.core.env.configuration import constants


class DeviceService:

    DEVICE_ID = uniqueid.id
        
    def vibrate_cb(self, time=1):
        
        try:
            vibrator.vibrate(time)
        except NotImplementedError:
            Logger.warn("No vibrate function defined for {} platform.".format(constants.PLATFORM))     
        else:
            Logger.info("RING!!")                      
        
    def notify_cb(self, title='', message='', timeout=1):
        
        notification.notify(
            title=title, 
            message=message, 
            app_name=constants.APP_NAME, 
            app_icon=os.path.join(constants.KIVY_RESOURCE_PATH_1, 'icon.png'),
            timeout=timeout
        )
        
        
