'''
Created on Jul 20, 2014

This file is part of CryptikChaos.

CryptikChaos is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CryptikChaos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CryptikChaos. If not, see <http://www.gnu.org/licenses/>.

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6.1"

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
        except (NotImplementedError, ImportError):
            Logger.warn(
                "DEVICE: No vibrate function defined for {} platform.".format(
                    constants.PLATFORM))     
        else:
            Logger.info("DEVICE: BUZZ!!")                      
        
    def notify_cb(self, title='', message='', timeout=1):
        
        try:
            notification.notify(
                title=title, 
                message=message, 
                app_name=constants.APP_NAME, 
                app_icon=os.path.join(constants.KIVY_RESOURCE_PATH_1, 'icon.png'),
                timeout=timeout
            )
        except (NotImplementedError, ImportError):
            Logger.warn(
                "DEVICE: No vibrate function defined for {} platform.".format(
                    constants.PLATFORM))     
        else:
            Logger.info("DEVICE: Fired Notification!")      
        
        
