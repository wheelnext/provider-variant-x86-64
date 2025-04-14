from __future__ import annotations

from typing import TYPE_CHECKING

import archspec.cpu

from variantlib.base import PluginType
from variantlib.base import VariantFeatureConfigType
from variantlib.base import VariantPropertyType
from variantlib.models.provider import VariantFeatureConfig

if TYPE_CHECKING:
    from collections.abc import Generator


class Plugin(PluginType):
    namespace = "x86_64"
    max_known_level = 4

    @staticmethod
    def _level_range(max_level: int) -> Generator[str]:
        for level in range(max_level, 0, -1):
            yield f"v{level}"

    def get_all_configs(self) -> list[VariantFeatureConfigType]:
        return [
            VariantFeatureConfig(
                "level", list(self._level_range(self.max_known_level))
            ),
        ]

    def get_supported_configs(self) -> list[VariantFeatureConfigType]:
        microarch = archspec.cpu.host().generic
        if microarch.name.startswith("x86_64_v"):
            supported_level = int(microarch.name.removeprefix("x86_64_v"))
            return [
                VariantFeatureConfig(
                    "level",
                    list(self._level_range(min(supported_level, self.max_known_level))),
                ),
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
