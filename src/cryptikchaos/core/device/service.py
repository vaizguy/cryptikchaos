'''
Created on Jul 20, 2014

@author: vaizguy
'''

__author__ = "Arun Vaidya"
__version__ = "0.6"

import plyer


class DeviceService:
    
    def __init__(self):
        
        self.DEVICE_ID = plyer.uniqueid.id
        
    def get_devid(self):
        
        return self.DEVICE_ID