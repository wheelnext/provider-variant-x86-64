from __future__ import annotations

from argparse import Namespace

import archspec.cpu
import pytest

from provider_variant_x86_64.plugin import X8664Plugin
from variantlib.models.provider import VariantFeatureConfig
from variantlib.models.variant import VariantProperty


@pytest.fixture
def plugin() -> X8664Plugin:
    return X8664Plugin()


def test_bulldozer_configs(mocker, plugin):
    mocker.patch("archspec.cpu.host").return_value = archspec.cpu.TARGETS["bulldozer"]
    assert plugin.get_supported_configs(None) == [
        VariantFeatureConfig("level", ["v2", "v1"]),
        VariantFeatureConfig("avx", ["on"]),
        VariantFeatureConfig("abm", ["on"]),
        VariantFeatureConfig("aes", ["on"]),
        VariantFeatureConfig("pclmulqdq", ["on"]),
        VariantFeatureConfig("sse4a", ["on"]),
        VariantFeatureConfig("sse4_2", ["on"]),
        VariantFeatureConfig("sse4_1", ["on"]),
        VariantFeatureConfig("ssse3", ["on"]),
        VariantFeatureConfig("sse3", ["on"]),
        VariantFeatureConfig("cx16", ["on"]),
        VariantFeatureConfig("sse2", ["on"]),
        VariantFeatureConfig("sse", ["on"]),
        VariantFeatureConfig("mmx", ["on"]),
    ]


def test_sandybridge_configs(mocker, plugin):
    mocker.patch("archspec.cpu.host").return_value = archspec.cpu.TARGETS["sandybridge"]
    assert plugin.get_supported_configs(None) == [
        VariantFeatureConfig("level", ["v2", "v1"]),
        VariantFeatureConfig("avx", ["on"]),
        VariantFeatureConfig("aes", ["on"]),
        VariantFeatureConfig("pclmulqdq", ["on"]),
        VariantFeatureConfig("sse4_2", ["on"]),
        VariantFeatureConfig("sse4_1", ["on"]),
        VariantFeatureConfig("ssse3", ["on"]),
        VariantFeatureConfig("sse3", ["on"]),
        VariantFeatureConfig("popcnt", ["on"]),
        VariantFeatureConfig("sse2", ["on"]),
        VariantFeatureConfig("sse", ["on"]),
        VariantFeatureConfig("mmx", ["on"]),
    ]


def test_generic_configs(mocker, plugin):
    mocker.patch("archspec.cpu.host").return_value = archspec.cpu.TARGETS["x86_64_v2"]
    assert plugin.get_supported_configs(None) == [
        VariantFeatureConfig("level", ["v2", "v1"]),
        VariantFeatureConfig("sse4_2", ["on"]),
        VariantFeatureConfig("sse4_1", ["on"]),
        VariantFeatureConfig("ssse3", ["on"]),
        VariantFeatureConfig("sse3", ["on"]),
        VariantFeatureConfig("cx16", ["on"]),
        VariantFeatureConfig("lahf_lm", ["on"]),
        VariantFeatureConfig("popcnt", ["on"]),
        VariantFeatureConfig("sse2", ["on"]),
        VariantFeatureConfig("sse", ["on"]),
        VariantFeatureConfig("mmx", ["on"]),
    ]


def test_non_x86_configs(mocker, plugin):
    mocker.patch("archspec.cpu.host").return_value = archspec.cpu.TARGETS["cortex_a72"]
    assert plugin.get_supported_configs(None) == []


def test_get_build_setup(plugin):
    assert plugin.get_build_setup(
        [
            VariantProperty("x86_64", "level", "v2"),
            VariantProperty("x86_64", "avx2", "on"),
        ]
    ) == {
        "cflags": ["-march=x86-64-v2"],
        "cxxflags": ["-march=x86-64-v2"],
    }


def test_get_build_setup_no_level(plugin):
    assert (
        plugin.get_build_setup(
            [
                VariantProperty("x86_64", "avx2", "on"),
            ]
        )
        == {}
    )


def test_get_build_setup_no_properties(plugin):
    assert plugin.get_build_setup([]) == {}


def test_level_cap(mocker, plugin):
    """Test that we do not return level higher than declared supported"""

    mocker.patch("archspec.cpu.host").return_value = Namespace(
        generic=Namespace(name="x86_64_v6")
    )
    assert plugin.get_supported_configs(None) == [
        VariantFeatureConfig("level", ["v4", "v3", "v2", "v1"]),
    ]
