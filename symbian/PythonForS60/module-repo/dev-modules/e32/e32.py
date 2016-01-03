# Copyright (c) 2009 Nokia Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from _e32 import *


class CapabilitySet:
    """This class enumerates all the capabilities present in TCapability class
       of symbian"""
    TCB, \
    CommDD, \
    PowerMgmt, \
    MultimediaDD, \
    ReadDeviceData, \
    WriteDeviceData, \
    DRM, \
    TrustedUI, \
    ProtServ, \
    DiskAdmin, \
    NetworkControl, \
    AllFiles, \
    SwEvent, \
    NetworkServices, \
    LocalServices, \
    ReadUserData, \
    WriteUserData, \
    Location, \
    SurroundingsDD, \
    UserEnvironment, \
    _None, \
    _Denied = range(22)


def get_capabilities():
    # API to get the capabilities of an application

    def get_logicalname(value):
    # Returns name of the capability
        for capas in dir(CapabilitySet):
            if getattr(CapabilitySet, capas) == value:
                return str(capas)

    capabilities = []
    tuple_of_capas = getcapability()
    for capas in tuple_of_capas:
        capabilities.append(get_logicalname(capas))
    result = tuple(capabilities)
    return result


def has_capabilities(arg):
    # API to check if the application has all the capabilities passed as a
    # list

    if not isinstance(arg, list):
        raise TypeError("Expected a list as an argument")
    my_list = []
    for capas in arg:
        try:
            capas_value = getattr(CapabilitySet, capas)
        except:
            raise ValueError("Invalid capability name: " + str(capas))
        my_list.append(capas_value)
    result = getcapability(my_list)
    return result
