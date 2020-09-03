from enum import Enum


class DeviceTypes(Enum):
    UNDEFINED, EVC, PHONE, HEADPHONES, LAPTOP = list(range(0, 5))


class EVCStatus(Enum):
    AUTHORIZATION = "Charger.EVC.Status.Authorization"
    CHARGE_POINT = "Charger.EVC.Status.ChargePoint"
    FIRMWARE_UPDATE = "Charger.EVC.Status.FirmwareUpdate"
    CHARGE_SESSION = "Charger.EVC.Status.ChargeSession"
    CURRENT_CHARGE_SESSION = "Charger.EVC.Status.CurrentChargeSession"
    CACHED_CHARGE_SESSION = "Charger.EVC.Status.CachedChargeSession"
    DELAY_CHARGE_REMAINING_TIME = "Charger.EVC.Status.DelayChargeRemainingTime"
    MASTER_CARD = "Charger.EVC.Status.MasterCard"
    USER_CARD = "Charger.EVC.Status.UserCard"
    METRICS = "Charger.EVC.Status.Metrics"
    MIN_CURRENT = "Charger.EVC.Status.MinCurrent"
    MAX_CURRENT = "Charger.EVC.Status.MaxCurrent"
    POWER_OPT_MIN = "Charger.EVC.Status.PowerOptimizerMin"
    POWER_OPT_MAX = "Charger.EVC.Status.PowerOptimizerMax"


class EVCSetting(Enum):
    TIMEZONE = "Charger.EVC.Setting.Timezone"
    LOCKABLE_CABLE = "Charger.EVC.Setting.LockableCable"
    AVAILABLE_CURRENT = "Charger.EVC.Setting.AvailableCurrent"
    POWER_OPTIMIZER = "Charger.EVC.Setting.PowerOptimizer"
    PLUG_AND_CHARGE = "Charger.EVC.Setting.PlugAndCharge"
    ETHERNET = "Charger.EVC.Setting.Ethernet"
    CELLULAR = "Charger.EVC.Setting.Cellular"


class EVCProgram(Enum):
    ECO_CHARGE = "Charger.EVC.Program.EcoCharge"
    DELAY_CHARGE = "Charger.EVC.Program.DelayCharge"


class EVCError(Enum):
    CONTRACTOR_WELDED = "Charger.EVC.Error.ContractorWelded"
    CONTRACTOR_RESPONSE = "Charger.EVC.Error.ContractorResponse"
    INTERLOCK_LOCK = "Charger.EVC.Error.InterlockLock"
    INTERLOCK_UNLOCK = "Charger.EVC.Error.InterlockUnlock"
    PP = "Charger.EVC.Error.PP"
    CP_DIODE = "Charger.EVC.Error.CpDiode"
    OVER_VOLTAGE_P1 = "Charger.EVC.Error.OverVoltageP1"
    OVER_VOLTAGE_P2 = "Charger.EVC.Error.OverVoltageP2"
    OVER_VOLTAGE_P3 = "Charger.EVC.Error.OverVoltageP3"
    UNDER_VOLTAGE_P1 = "Charger.EVC.Error.UnderVoltageP1"
    UNDER_VOLTAGE_P2 = "Charger.EVC.Error.UnderVoltageP2"
    UNDER_VOLTAGE_P3 = "Charger.EVC.Error.UnderVoltageP3"
    OVER_CURRENT_P1 = "Charger.EVC.Error.OverCurrentP1"
    OVER_CURRENT_P2 = "Charger.EVC.Error.OverCurrentP2"
    OVER_CURRENT_P3 = "Charger.EVC.Error.OverCurrentP3"
    RESIDUAL_CURRENT = "Charger.EVC.Error.ResidualCurrent"
    PROTECTIVE_EARTH = "Charger.EVC.Error.ProtectiveEarth"
    RFID = "Charger.EVC.Error.Rfid"
    INTERLOCK_PERMANENT = "Charger.EVC.Error.InterlockPermanent"
    OCP_PERMANENT = "Charger.EVC.Error.OcpPermanent"
    LOAD_BALANCE_MODULE_1 = "Charger.EVC.Error.LoadBalanceModule1"
    LOAD_BALANCE_MODULE_2 = "Charger.EVC.Error.LoadBalanceModule2"
    LOAD_BALANCE_MODULE_3 = "Charger.EVC.Error.LoadBalanceModule3"
    HMI_EXTERNAL = "Charger.EVC.Error.HmiExternal"
