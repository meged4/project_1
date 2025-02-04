import enum


class FabricatorEnum(enum.Enum):
    Makita = "Makita"
    DeWalt = "DeWalt"
    Milwaukee = "Milwaukee"


class PowerTypeEnum(enum.Enum):
    ot_seti = "От сети"
    akkumuljator = "От аккумулятора"
    szhatiy_vozduh = "Сжатый воздух"
    benzinoviy = "Бензиновый двигатель"