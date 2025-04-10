from variantlib.base import PluginType
from variantlib.base import VariantFeatureConfigType
from variantlib.models.provider import VariantFeatureConfig


class Plugin(PluginType):
    namespace = "x86_64"

    def get_all_configs(self) -> list[VariantFeatureConfigType]:
        return [
            VariantFeatureConfig("level", ["v4", "v3", "v2", "v1"]),
        ]

    def get_supported_configs(self) -> list[VariantFeatureConfigType]:
        # TODO: do CPU detection, fitler
        return self.get_all_configs()
