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


from _sensorfw import *
from sensor_defs import *


class _Channel:
    '''Define _Channel Python class, access to low level sensor data.'''

    def __init__(self, channel_id):
        self.__channel_id = channel_id
        self.__channel = open_channel(self.__channel_id)
        self.__data_event_callback = None
        self.__data_error_callback = None
        self.__data_listening = False

    def start_data_listening(self, event_cb, error_cb):
        self.__data_event_callback = event_cb
        self.__data_error_callback = error_cb
        data_listening = self.__channel.start_data_listening(self.__data_event_callback, self.__data_error_callback)
        self.__data_listening = data_listening
        return data_listening

    def stop_data_listening(self):
        not_data_listening = self.__channel.stop_data_listening()
        self.__data_listening = not not_data_listening
        return not_data_listening

    def is_data_listening(self):
        return self.__data_listening

    def channel_id(self):
        return self.__channel_id

    def properties(self):
        return self.__channel.get_all_properties()

    def set_property(self, property_id, item_index, array_index, value):
        return self.__channel.set_property(property_id, item_index, array_index, value)

#
# filter classes
#


class _filterBase:

    def __init__(self, windowLen=10, dimensions=3):
        self.windowLen = windowLen
        self.dimensions = dimensions

        # initialize data buffer
        self.buffer = [0] * dimensions
        for t in range(dimensions):
            self.buffer[t] = [0] * self.windowLen

        self.pointer = 0

    def updateBuffer(self, *data):
        self.result = [0] * self.dimensions
        for t in range(self.dimensions):
            self.buffer[t][self.pointer] = data[t]
        self.pointer += 1
        self.pointer = self.pointer % self.windowLen


class DummyFilter(_filterBase):

    def filter(self, *data):
        return data


class MedianFilter(_filterBase):

    def filter(self, *data):
        self.updateBuffer(*data)

        for t in range(self.dimensions):
            tmp = self.buffer[t][:]
            tmp.sort()
            self.result[t] = tmp[self.windowLen/2]

        return self.result


class LowPassFilter(_filterBase):

    def filter(self, *data):
        self.updateBuffer(*data)

        for t in range(self.dimensions):
            self.result[t] = int(self.sum(self.buffer[t]) / self.windowLen)

        return self.result

    def sum(self, buff):
        # default sum() function is not avaialble in s60
        return reduce(lambda x, y: x+y, buff)


def list_channels():
    result = []
    # Get all available sensor channels
    _channels = channels()

    # store basic information about each sensor channel
    for channel_id, channel_info in _channels.items():
        channel_name = get_logicalname(KSensrvChannelTypeId, channel_info['channel_type'])
        result.append({
            'id': channel_id,
            'type': channel_info['channel_type'],
            'name': channel_name})

    return result

#
# generic sensor classes
#


class _Sensor:
    channelID = None

    def __init__(self, data_filter=None):
        if data_filter is None:
            data_filter = DummyFilter()
        self.filter = data_filter

        self._channels = []
        self.listening = 0
        self.channel = None
        self._counter = 0
        self.data_callback = None
        self.error_callback = None
        self._channels = list_channels()

    def set_callback(self, data_callback, error_callback=None):
        self.data_callback = data_callback
        self.error_callback = error_callback

    def custom_cb(self):
        if self.data_callback is not None:
            self.data_callback()

    def error_cb(self, error):
        ''' Error callback function'''
        if self.error_callback is not None:
            self.error_callback(error)

    def _listChannelProperties(self, channel):
        # generates printout for debuggin purposes
        channelProperties = channel.properties()
        for t in channelProperties:
            propertyId, arrayIndex, itemIndex = t

            if arrayIndex < 0:
                arrayIndex = get_logicalname(TSensrvArrayIndex, arrayIndex)

            print get_logicalname(KSensrvPropId, propertyId), \
                  get_logicalname(TSensrvPropertyType, channelProperties[t]['property_type']),\
                  arrayIndex, itemIndex

            print channelProperties[t]
            print

    def _getChannelProperty(self, channel, property_id=None):
        result = {}
        channel_properties = channel.properties()
        for t in channel_properties:
            channel_property_id, array_index, item_index = t
            if property_id is None or property_id == channel_property_id:
                result[t] = channel_properties[t]
        return result

    def set_property(self, property_id, value, property_item_index=-1):
        if self.channelID is not None:
            # open channel if it is not yet opened
            if self.channel is None:
                self._openchannel(self.channelID)
        channel_properties = self._getChannelProperty(self.channel, property_id)
        for prop in channel_properties:
            if property_id == channel_properties[prop]['property_id']:
                break
        array_index = channel_properties[prop]['property_array_index']
        self.channel.set_property(property_id, property_item_index,
                                  array_index, value)


    def get_property(self, property_id=None, property_item_index=-1):
        if self.channelID is not None:
            # open channel if it is not yet opened
            if self.channel is None:
                self._openchannel(self.channelID)

        channel_properties = self._getChannelProperty(self.channel, property_id)
        for prop in channel_properties:
            prop_id = get_logicalname(KSensrvPropId,
                                      channel_properties[prop]['property_id'])
            prop_value_type = get_logicalname(TSensrvPropertyType,
                                      channel_properties[prop]['property_type'])
            read_only = bool(channel_properties[prop]['read_only'])
            if channel_properties[prop]['property_array_index'] == -1:
                prop_type = 'SingleProperty'
            elif channel_properties[prop]['property_array_index'] == -2:
                prop_type = 'ArrayProperty'
            else:
                prop_type = channel_properties[prop]['property_array_index']
            result = channel_properties[prop]
            result.update({'property_id': prop_id,
                           'read_only': read_only,
                           'property_array_index': prop_type})
            result.pop('property_type')
            print result


    def start_listening(self):
        if self.channelID is not None:
            # open channel if it is not yet opened
            if self.channel is None:
                self._openchannel(self.channelID)

            # start listening if not yet listening
            if self.listening != 1:
                self._startlistening(self.data_cb)
                return True

        return False

    def _openchannel(self, channel_id):
        if self.channel != None:
            return False # only one channel per instance allowed now

        for t in self._channels:
            if t['type'] == channel_id:
                self.channel = _Channel(t['id'])
                return self.channel

        return False

    def _startlistening(self, cb):
        if self.channel is not None and self.listening != 1:
            self.listening = self.channel.start_data_listening(cb, self.error_cb)
            if self.listening == 1:
                return True # success

        return False # failed

    def stop_listening(self):
        if self.channel is not None and self.listening == 1:
            self.channel.stop_data_listening()
            self.channel = None
            self.listening = 0

    def data_cb(self, data):
        # override this function
        # unpack data and store it
        # call self.custom_cb() in the end
        self.custom_cb()


class _StreamDataSensor(_Sensor):

    def get_available_data_rates(self):
        # returns available datarates as list. Number order in list corresponds array_index numbers

        dataRateProperties = self._getChannelProperty(self.channel, KSensrvPropId.DataRate)
        dataRates = [0] * (len(dataRateProperties) - 1)

        for dataRateProperty in dataRateProperties:
            propertyKey, propertyValue = dataRateProperty
            if propertyValue['property_array_index'] >= 0:
                dataRates[propertyValue['property_array_index']] = propertyValue['value']

        return dataRates

    def get_data_rate(self):
        # returns current data rate
        properties = self.channel.properties()

        dataRateIndex = properties[(KSensrvPropId.DataRate,
                                   TSensrvArrayIndex.ESensrvArrayPropertyInfo,
                                   -1)]['value']

        availableDataRates = self.get_available_data_rates()

        return availableDataRates[dataRateIndex]

    def set_data_rate(self, datarate):
        availableDataRates = self.get_available_data_rates()
        if datarate not in availableDataRates:
            return False
        # set property, NOTE/FIXME parameter order in wrapper is : id, arrayind, itemind, value
        self.channel.set_property(KSensrvPropId.DataRate,
                                  -1,
                                  TSensrvArrayIndex.ESensrvArrayPropertyInfo,
                                  availableDataRates.index(datarate))
        return True


class _AccelerometerSensor(_StreamDataSensor):

    def set_measure_range(self, measurerange):
        # hackish way to set range
        # 0 = +-2g
        # 1 = +-8g
        self.channel.set_property(KSensrvPropId.MeasureRange, -1,
                                  TSensrvArrayIndex.ESensrvArrayPropertyInfo, DATARANGE2G)

    def get_measure_range(self, measurerange):
        # hackish way to get range
        # 0 = +-2g
        # 1 = +-8g
        return self.channel.properties()[KSensrvPropId.MeasureRange,
                                         TSensrvArrayIndex.ESensrvArrayPropertyInfo,
                                         -1]['value']


#
# sensor spesific classes
#

# FIXME : check always that channel actually exists


class AmbientLightData(_Sensor):
    channelID = KSensrvChannelTypeId.AmbientLightData
    ambient_light = 0

    def data_cb(self, data):
        self.ambient_light = data['iAmbientLight']
        self.custom_cb()


class ProximityMonitor(_Sensor):
    channelID = KSensrvChannelTypeId.ProximityMonitor
    proximity_state = 0

    def data_cb(self, data):
        self.proximity_state = data['iProximityState']
        self.custom_cb()


class OrientationData(_Sensor):
    channelID = KSensrvChannelTypeId.OrientationData
    device_orientation = -1

    def data_cb(self, data):
        self.device_orientation = data['orientation']
        self.custom_cb()


class MagneticNorthData(_Sensor):
    azimuth = 0
    channelID = KSensrvChannelTypeId.MagneticNorthData

    def data_cb(self, data):
        self.azimuth = data["yaw"]
        self.custom_cb()


class MagnetometerXYZAxisData(_Sensor):
    channelID = KSensrvChannelTypeId.MagnetometerXYZAxisData
    x, y, z = 0, 0, 0
    calib_level = 0

    def data_cb(self, data):
        x, y, z = data["axis_x_calib"], data["axis_y_calib"], data["axis_z_calib"]
        #x,y,z = data["axis_x_raw"], data["axis_y_raw"], data["axis_z_raw"]
        self.x, self.y, self.z = self.filter.filter(x, y, z)

        properties = self.channel.properties()
        calib_property = properties[(KSensrvPropId.KSensrvPropCalibrationLevel,
                                     -1,
                                     TSensrvArrayIndex.ESensrvSingleProperty)]

        self.calib_level = calib_property['value']

        self.custom_cb()


class AccelerometerDoubleTappingData(_AccelerometerSensor):
    channleID = KSensrvChannelTypeId.AccelerometerDoubleTappingData
    direction = 0

    def __init__(self, *args, **kwargs):
        _Sensor.__init__(self, *args, **kwargs)
        # open channel already here so it is possible to configure property values
        # before starting to listen
        self._openchannel(KSensrvChannelTypeId.AccelerometerDoubleTappingData)

    def data_cb(self, data):
        self.direction = data["direction"]
        self.custom_cb()

    # FIXME, remove this and use listen method from base class

    def start_listening(self):
        return self._startlistening(self.data_cb)

    def get_axis_active(self):
        # returns 1 if axis is active, otherwise 0.
        properties = self.channel.properties()

        x, y, z = [properties[(KSensrvPropId.AxisActive,
                             TSensrvArrayIndex.ESensrvSingleProperty, t)]['value']
                 for t in range(1, 4)]

        return x, y, z

    def get_properties(self):
        properties = self.channel.properties()

        DblTapThresholdValue = properties[(KSensrvPropId.DblTapThreshold, -1,
                                           TSensrvArrayIndex.ESensrvSingleProperty)]['value']

        DblTapDurationValue = properties[(KSensrvPropId.DblTapDuration, -1,
                                          TSensrvArrayIndex.ESensrvSingleProperty)]['value']

        DblTapLatencyValue = properties[(KSensrvPropId.DblTapLatency, -1,
                                         TSensrvArrayIndex.ESensrvSingleProperty)]['value']

        DblTapIntervalValue = properties[(KSensrvPropId.DblTapInterval, -1,
                                          TSensrvArrayIndex.ESensrvSingleProperty)]['value']

        return DblTapThresholdValue, \
               DblTapDurationValue, \
               DblTapLatencyValue, \
               DblTapIntervalValue

    def set_axis_active(self, x=None, y=None, z=None):
        if x is not None:
            self.channel.set_property(KSensrvPropId.AxisActive, 1,
                                      TSensrvArrayIndex.ESensrvSingleProperty,
                                      x)

        if y is not None:
            self.channel.set_property(KSensrvPropId.AxisActive, 2,
                                      TSensrvArrayIndex.ESensrvSingleProperty,
                                      y)
        if z is not None:
            self.channel.set_property(KSensrvPropId.AxisActive, 3,
                                      TSensrvArrayIndex.ESensrvSingleProperty,
                                      z)

    def set_properties(self,
                      DblTapThresholdValue=None,
                      DblTapDurationValue=None,
                      DblTapLatencyValue=None,
                      DblTapIntervalValue=None):

        if DblTapThresholdValue is not None:
            self.channel.set_property(KSensrvPropId.DblTapThreshold,
                                      -1,
                                      TSensrvArrayIndex.ESensrvSingleProperty,
                                      DblTapThresholdValue)

        if DblTapDurationValue is not None:
            self.channel.set_property(KSensrvPropId.DblTapDuration,
                                      -1,
                                      TSensrvArrayIndex.ESensrvSingleProperty,
                                      DblTapDurationValue)

        if DblTapLatencyValue is not None:
            self.channel.set_property(KSensrvPropId.DblTapLatency,
                                      -1,
                                      TSensrvArrayIndex.ESensrvSingleProperty,
                                      DblTapLatencyValue)

        if DblTapIntervalValue is not None:
            self.channel.set_property(KSensrvPropId.DblTapInterval,
                                      -1,
                                      TSensrvArrayIndex.ESensrvSingleProperty,
                                      DblTapIntervalValue)


class AccelerometerXYZAxisData(_AccelerometerSensor):
    channelID = KSensrvChannelTypeId.AccelerometerXYZAxisData
    x, y, z = 0, 0, 0

    def data_cb(self, data):
        x, y, z = data["axis_x"], data["axis_y"], data["axis_z"]
        self.x, self.y, self.z = self.filter.filter(x, y, z)

        self.custom_cb()

class RotationData(_Sensor):
    channelID = KSensrvChannelTypeId.RotationData
    x, y, z = 0, 0, 0

    def data_cb(self, data):
        x, y, z = data["axis_x"], data["axis_y"], data["axis_z"]
        self.x, self.y, self.z = self.filter.filter(x, y, z)

        self.custom_cb()
