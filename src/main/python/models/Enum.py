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

