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

class KSensrvChannelTypeId:
    # sensor server channels
    AccelerometerXYZAxisData            = 0x1020507E # sensrvaccelerometersensor.h
    AmbientLightData                    = 0x2000BF16 # sensrvilluminationsensor.h
    MagneticNorthData                   = 0x2000BEDF # sensrvmagneticnorthsensor.h
    MagnetometerXYZAxisData             = 0x2000BEE0 # sensrvmagnetometersensor.h
    OrientationData                     = 0x10205088 # sensrvorientationsensor.h
    RotationData                        = 0x10205089 # sensrvorientationsensor.h
    ProximityMonitor                    = 0x2000E585 # sensrvproximitysensor.h
    TSensrvTappingData                  = 0x1020507F # sensrvtappingsensor.h
    AccelerometerDoubleTappingData      = 0x10205081 # sensrvtappingsensor.h
    Undefined                           = 0x00000000 # sensrvtypes.h

class KSensrvPropId:
    # sensor server channel properties
    AxisActive                          = 0x00001001 # sensrvaccelerometersensor.h
    DataRate                            = 0x00000002 # sensrvgeneralproperties.h
    Power                               = 0x01001003 # sensrvgeneralproperties.h
    Availability                        = 0x00000004 # sensrvgeneralproperties.h
    MeasureRange                        = 0x00000005 # sensrvgeneralproperties.h
    ChannelDataFormat                   = 0x000000006 # sensrvgeneralproperties.h
    ScaledRange                         = 0x000000007 # sensrvgeneralproperties.h
    ChannelAccuracy                     = 0x000000008 # sensrvgeneralproperties.h
    ChannelScale                        = 0x000000009 # sensrvgeneralproperties.h
    ChannelUnit                         = 0x0000000010 # sensrvgeneralproperties.h
    DblTapThreshold                     = 0x00001002 # sensrvtappingsensor.h
    DblTapDuration                      = 0x00001003 # sensrvtappingsensor.h
    DblTapLatency                       = 0x00001004 # sensrvtappingsensor.h
    DblTapInterval                      = 0x00001005 # sensrvtappingsensor.h
    AutoCalibrationActive               = 0x00001006 # sensrvmagnetometersensor.h
    CalibrationLevel                    = 0x00001007 # sensrvmagnetometersensor.h
    #DblTapAxisActive = AxisActive
    SensorModel                               = 0x0000000011 # sensrvgeneralproperties.h
    SensorConnectionType                      = 0x0000000012 # sensrvgeneralproperties.h
    SensorDescription                         = 0x0000000013 # sensrvgeneralproperties.h


# The connection type of sensor.
#
# Possible values:
# - ESensrvConnectionTypeNotDefined, Connection type is not defined
# - ESensrvConnectionTypeEmbedded, Sensor is embedded in Handset
# - ESensrvConnectionTypeWired for sensors which are attached to handset with wire
# - ESensrvConnectionTypeWireless for sensors which are attached to handset wireless
# - ESensrvConnectionTypeLicenseeBase, start of licensee connection type range. 
# - ESensrvConnectionTypeLicenseeEnd, end of licensee connection type range.

class TSensrvConnectionType:
    ESensrvConnectionTypeNotDefined = 0
    ESensrvConnectionTypeEmbedded = 1
    ESensrvConnectionTypeWired = 2
    ESensrvConnectionTypeWireless = 3
    ESensrvConnectionTypeLicenseeBase = 8192
    ESensrvConnectionTypeLicenseeEnd = 12287 


# sensrvproperty.h
class TSensrvPropertyType:
    ESensrvUninitializedProperty = 0
    ESensrvIntProperty = 1
    ESensrvRealProperty = 2
    ESensrvBufferProperty = 3

class TSensrvArrayIndex:
    ESensrvSingleProperty    = -1
    ESensrvArrayPropertyInfo = -2    

class TSensrvPropertyRangeUsage:
    # General properties owned and defined by the framework
    ESensrvPropertyRangeNotDefined = 0, # 0x0000
    ESensrvGeneralPropertyRangeBase = 1, # 0x0001
    ESensrvGeneralPropertyRangeEnd = 4095, # 0x0FFF

    # Channel properties defined by each sensor package.
    # These are not unique across all channels
    ESensrvChannelPropertyRangeBase = 4096, # 0x1000
    ESensrvChannelPropertyRangeEnd = 8191, # 0x1FFF

    # A range for licensees to define their own properties. 
    # Usage is defined by the licensee. 
    ESensrvLicenseePropertyRangeBase = 8192, # 0x2000
    ESensrvLicenseePropertyRangeEnd = 12287 # 0x2FFF

# sensrvtypes.h
class TSetPropertySuccessIndicator:
    ESetPropertyIndicationUnknown, \
    ESetPropertyIndicationAvailable, \
    ESetPropertyIndicationPossible, \
    ESetPropertyIndicationUnavailable = range(4)

"""
/**
* The quantity of channel values. Defines the quantity the channel is measuring. 
*
* Possible values:
* - ESensrvQuantityNotUsed, Channel doesn't provide this information.
* - ESensrvQuantityNotdefined quantity is not defined.
* - ESensrvQuantityAcceleration Channel measures acceleration 
* - ESensrvQueantityTapping Channel measures tapping events 
* - ESensrvQuantityOrientation Channel measures phone orientation
* - ESensrvQuantityRotation Channel measures phone rotation
* - ESensrvQuantityMagnetic
* - ESensrvQuantityAngle
* - ESensrvQuantityLicenseeBase, start of licensee quantity range. 
* - ESensrvQuantityLicenseeEnd, end of licensee quantity range. 
*
*/
"""
class TSensrvQuantity:
    ESensrvQuantityNotUsed = -1,
    ESensrvQuantityNotdefined = 0,
    ESensrvQuantityAcceleration = 10,
    ESensrvQuantityTapping = 11,
    ESensrvQuantityOrientation = 12,
    ESensrvQuantityRotation = 13,
    ESensrvQuantityMagnetic = 14,
    ESensrvQuantityAngle = 15,
    ESensrvQuantityProximity = 16,
    ESensrvQuantityLicenseeBase = 8192,
    ESensrvQuantityLicenseeEnd = 12287

"""
/**
* The context type of sensor.
*
* Possible values:
* - ESensrvContextTypeNotUsed, Channel doesn't provide this information.
* - ESensrvContextTypeNotdefined, Context type is not defined
* - ESensrvContextTypeAmbient for category contains sensors measuring some generic, 
*   common features of the environment such as pressure or temperature of the air, 
*   sound intensity, or state of the weather. 
* - ESensrvContextTypeDevice for sensors, which are producing information of the device itself. 
* - ESensrvContextTypeUser for sensors which are measuring user initiated stimulus (gesture), 
*   or characteristics/properties of the user (body temperature, mass, heart rate).
* - ESensrvContextTypeLicenseeBase, start of licensee context type range. 
* - ESensrvContextTypeLicenseeEnd, end of licensee context type range. 
*
*/
"""
class TSensrvContextType:
    ESensrvContextTypeNotUsed = -1,
    ESensrvContextTypeNotDefined = 0,    
    ESensrvContextTypeAmbient = 1,
    ESensrvContextTypeDevice = 2,
    ESensrvContextTypeUser = 3,
    ESensrvContextTypeLicenseeBase = 8192,
    ESensrvContextTypeLicenseeEnd = 12287

"""
/**
* The connection type of sensor.
*
* Possible values:
* - ESensrvConnectionTypeNotDefined, Connection type is not defined
* - ESensrvConnectionTypeEmbedded, Sensor is embedded in Handset
* - ESensrvConnectionTypeWired for sensors which are attached to handset with wire
* - ESensrvConnectionTypeWireless for sensors which are attached to handset wireless
* - ESensrvConnectionTypeLicenseeBase, start of licensee connection type range. 
* - ESensrvConnectionTypeLicenseeEnd, end of licensee connection type range. 
*
*/
"""
class TSensrvConnectionType:
    ESensrvConnectionTypeNotDefined = 0,
    ESensrvConnectionTypeEmbedded = 1,
    ESensrvConnectionTypeWired = 2,
    ESensrvConnectionTypeWireless = 3,
    ESensrvConnectionTypeLicenseeBase = 8192,
    ESensrvConnectionTypeLicenseeEnd = 12287

"""
/**
* The TSensrvChannelUnit represents the unit of the measured data values.
*
* Possible values:
* - ESensrvChannelUnitNotDefined, Unit is not defined
* - ESensevChannelUnitAcceleration, Acceleration, meter per square second (m/s^2)
* - ESensrvChannelUnitGravityConstant, Acceleration, gravitational constant (G)
* - ESensrvChannelUnitLicenseeBase, start of licensee channel unit range. 
* - ESensrvChannelUnitLicenseeEnd, end of licensee channel unit range. 
*
*/
"""
class TSensrvChannelUnit:
    ESensrvChannelUnitNotDefined = 0,
    ESensevChannelUnitAcceleration = 10,         
    ESensrvChannelUnitGravityConstant = 11,
    ESensrvChannelUnitLicenseeBase = 8192,
    ESensrvChannelUnitLicenseeEnd = 12287

"""
/**
* The format of the data is represented in a channel data structure.
*
* Possible values:
* - ESensrvChannelDataFormatAbsolute, value of the data item represents actual value of 
*   the measured quantity.
* - ESensrvChannelDataFormatScaled, value of the data item represents relative value which
*   is scaled to between maximum and minimum value of the measured quantity. 
*   KSensrvPropIdScaledRange defines range for the data item value and 
*   KSensrvPropIdMeasureRange defines range for the measured quantity.
* - ESensrvChannelDataFormatLicenseeBase, start of licensee channel data format range. 
* - ESensrvChannelDataFormatLicenseeEnd, end of licensee channel data format range. 
*
@code 
Scaled format example:
Measure range for the accelerometer, KSensrvPropIdMeasureRange: -2g to 2g.
KSensrvPropIdScaledRange defines following values:
Range: Min: -127  Max: 127

Example values for the data item and their absolute values:
Data item: -64 = > -64/127 * 2g = -1.01g
Data item:  32 = > 32/127 * 2g = 0.51g
Data item: 127 = > 127/127 * 2g = 2g
@endcode
*   @see KSensrvPropIdChannelDataBitCount 
*
*/
"""
class TSensrvChannelDataFormat:
    ESensrvChannelDataFormatNotDefined = 0,
    ESensrvChannelDataFormatAbsolute = 1,
    ESensrvChannelDataFormatScaled = 2,
    ESensrvChannelDataFormatLicenseeBase = 8192,
    ESensrvChannelDataFormatLicenseeEnd = 12287

"""
/**
* The TSensrvErrorSeverity represents sensor server error code which can occur in 
* sensor listeners.
*
* Possible values:
* - ESensrvErrorSeverityMinor, some async request(s) failed. If this is not followed
*   by ESensrvFatal, it means listening has been successfully continued. 
* - ESensrvErrorSeverityFatal, fatal error, server internal state regarding this channel might 
*   be corrupted. The channel was closed and sensor server session terminated.
*/
"""
class TSensrvErrorSeverity:
    ESensrvErrorSeverityNotDefined, \
    ESensrvErrorSeverityMinor, \
    ESensrvErrorSeverityFatal = range(3)

"""
/**
* The type of channel change detected.
*
* Possible values:
* - ESensrvChannelChangeTypeNotDefined, a channel not defined
* - ESensrvChannelChangeTypeRemoved, a channel was removed
* - ESensrvChannelChangeTypeAdded, a new channel was added
*/
"""
class TSensrvChannelChangeType:
    ESensrvChannelChangeTypeNotDefined, \
    ESensrvChannelChangeTypeRemoved, \
    ESensrvChannelChangeTypeAdded = range(3)

# sensrvchannelcondition.h
class TSensrvConditionType:
    ESensrvSingleLimitCondition, \
    ESensrvRangeConditionLowerLimit, \
    ESensrvRangeConditionUpperLimit, \
    ESensrvBinaryCondition = range(4)

class TSensrvConditionOperator:
    ESensrvOperatorEquals, \
    ESensrvOperatorGreaterThan, \
    ESensrvOperatorGreaterThanOrEquals, \
    ESensrvOperatorLessThan, \
    ESensrvOperatorLessThanOrEquals, \
    ESensrvOperatorBinaryAnd, \
    ESensrvOperatorBinaryAll = range(7)

# sensrvchannelconditionset.h
class TSensrvConditionSetType:
    ESensrvOrConditionSet = 0
    ESensrvAndConditionSet = 1


### Sensor specific definition
# sensrvtappingsensor.h
class KSensrvAccelerometerDirection:
    Xplus   = 0x01
    Xminus  = 0x02
    X       = 0x03
    Yplus   = 0x04
    Yminus  = 0x08
    Y       = 0x0c
    Zplus   = 0x10
    Zminus  = 0x20
    Z       = 0x30


# sensrvproximitysensor.h
class TProximityState:
    EProximityUndefined = 0
    EProximityIndiscernible = 1
    EProximityDisc = 2

# sensrvorientationsensor.h
class TSensrvDeviceOrientation:
    #Possible device orientations
    EOrientationUndefined, \
    EOrientationDisplayUp, \
    EOrientationDisplayDown, \
    EOrientationDisplayLeftUp, \
    EOrientationDisplayRightUp, \
    EOrientationDisplayUpwards, \
    EOrientationDisplayDownwards = range(7)
    KSensrvRotationUndefined = -1

# sensrvilluminationsensor.h
class TSensrvAmbientLightData:
    KAmbientLightVeryDark 	= 0
    KAmbientLightDark 	    = 20
    KAmbientLightTwilight 	= 40
    KAmbientLightLight      = 60
    KAmbientLightBright     = 80
    KAmbientLightSunny      = 100
    
# function for querying logical name based on number
def get_logicalname(classObject, constantNumber):
    # returns name of constant
    for t in dir (classObject):
        if getattr(classObject, t) == constantNumber:
            return t
    return None    

if __name__ == '__main__':
    # self test & example
    assert get_logicalname(KSensrvChannelTypeId, 0x1020507E) == 'AccelerometerXYZAxisData'
