from enum import Enum

class DDSTextureFormat(Enum):
    BC1_UNORM = 0
    BC1_UNORM_SRGB = 1
    BC2_UNORM = 2
    BC2_UNORM_SRGB = 3
    BC3_UNORM = 4
    BC3_UNORM_SRGB = 5
    BC4_UNORM = 6
    BC4_SNORM = 7
    BC5_UNORM = 8
    BC5_SNORM = 9
    BC6H_UF16 = 10
    BC6H_SF16 = 11
    BC7_UNORM = 12
    BC7_UNORM_SRGB = 13
    R8G8B8A8_UNORM = 14
    R8G8B8A8_UNORM_SRGB = 15

class AlphaMethod(Enum):
    PREMULTIPLIED = "-pmalpha"
    STRAIGHT = "-alpha"
    SEPERATE = "-sepalpha"

class Preset(Enum):
    ALBEDO = 0,
    NORMAL = 1,
    MATERIAL = 2
    FX = 3
