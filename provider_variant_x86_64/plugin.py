from __future__ import annotations

from typing import TYPE_CHECKING

import archspec.cpu

from variantlib.models.provider import VariantFeatureConfig
from variantlib.protocols import PluginType
from variantlib.protocols import VariantFeatureConfigType
from variantlib.protocols import VariantPropertyType

if TYPE_CHECKING:
    from collections.abc import Generator


class X8664Plugin(PluginType):
    namespace = "x86_64"

    max_known_level = 4
    """Max microarchitecture level supported at the time"""

    all_features = [
        # zen5 features features
        "avx_vnni",
        "cppc",
        "ibrs_enhanced",
        "tsc_adjust",
        # zen4 features features
        "flush_l1d",
        # sapphirerapids features
        "movdir64b",
        "movdiri",
        # icelake features
        "avx512_bf16",
        "avx512_bitalg",
        "avx512_vbmi2",
        "avx512_vnni",
        "avx512_vp2intersect",
        "avx512_vpopcntdq",
        "avx512ifma",
        "avx512vbmi",
        "rdpid",
        "sha_ni",
        "vaes",
        "vpclmulqdq",
        # skylake_avx512 features
        "clwb",
        "clzero",
        # x86-64-v4 features
        "avx512bw",
        "avx512cd",
        "avx512dq",
        "avx512f",
        "avx512vl",
        # skylake features
        "clflushopt",
        "gfni",
        "rdseed",
        "xsavec",
        "xsaveopt",
        # broadwell features
        "adx",
        # x86-64-v3 features
        "avx2",
        "avx",
        "bmi2",
        "bmi1",
        "abm",
        "f16c",
        "fma",
        "movbe",
        "xsave",
        # sandybridge features
        "rdrand",
        # westmere features
        "aes",
        # nehalem features
        "pclmulqdq",
        # steamroller features
        "sse4a",
        "fsgsbase",
        # x86-64-v2 features
        "sse4_2",
        "sse4_1",
        "ssse3",
        "sse3",
        "cx16",
        "lahf_lm",
        "popcnt",
        # x86-64-v1 features
        "sse2",
        "sse",
        "mmx",
    ]
    """All features supported by archspec at the time, sorted in preference order"""

    @staticmethod
    def _level_range(max_level: int) -> Generator[str]:
        for level in range(max_level, 0, -1):
            yield f"v{level}"

    def get_all_configs(self) -> list[VariantFeatureConfigType]:
        return [
            VariantFeatureConfig(
                "level", list(self._level_range(self.max_known_level))
            ),
        ] + [VariantFeatureConfig(feature, ["on"]) for feature in self.all_features]

    def get_supported_configs(self) -> list[VariantFeatureConfigType]:
        microarch = archspec.cpu.host()
        generic = microarch.generic
        if generic.name.startswith("x86_64_v"):
            supported_level = int(generic.name.removeprefix("x86_64_v"))
            return [
                VariantFeatureConfig(
                    "level",
                    list(self._level_range(min(supported_level, self.max_known_level))),
                ),
            ] + [
                VariantFeatureConfig(feature, ["on"])
                for feature in self.all_features
                if feature in microarch
            ]

        return []

    def get_build_setup(
        self, properties: list[VariantPropertyType]
    ) -> dict[str, list[str]]:
        for prop in properties:
            assert prop.namespace == self.namespace
            if prop.feature == "level":
                flag = f"-march=x86-64-{prop.value}"
                if prop.value == "v1":
                    flag = "-march=x86-64"
                return {
                    "cflags": [flag],
                    "cxxflags": [flag],
                }
        return {}
