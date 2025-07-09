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


def test_get_compiler_flags(plugin):
    assert plugin.get_compiler_flags(
        "c",
        "gcc",
        "14.3.0",
        [
            VariantProperty("x86_64", "level", "v2"),
            VariantProperty("x86_64", "avx2", "on"),
        ],
    ) == ["-march=x86-64-v2"]


def test_get_compiler_flags_no_level(plugin):
    assert (
        plugin.get_compiler_flags(
            "c++",
            "clang",
            "20.1.8",
            [
                VariantProperty("x86_64", "avx2", "on"),
            ],
        )
        == []
    )


def test_get_compiler_flags_no_properties(plugin):
    assert plugin.get_compiler_flags("c", "clang", "19.1.7", []) == []


def test_level_cap(mocker, plugin):
    """Test that we do not return level higher than declared supported"""

    mocker.patch("archspec.cpu.host").return_value = Namespace(
        generic=Namespace(name="x86_64_v6")
    )
    assert plugin.get_supported_configs(None) == [
        VariantFeatureConfig("level", ["v4", "v3", "v2", "v1"]),
    ]


@pytest.mark.parametrize(
    "vprop",
    [
        "x86_64 :: level :: v1",
        "x86_64 :: level :: v4",
        "x86_64 :: avx512f :: on",
        "x86_64 :: sse3 :: on",
        "x86_64 :: ssse3 :: on",
    ],
)
def test_validate_variant(vprop: str, plugin) -> None:
    assert plugin.validate_property(VariantProperty.from_str(vprop))


@pytest.mark.parametrize(
    "vprop",
    [
        "x86_64 :: level :: v5",
        "x86_64 :: level :: v0",
        "x86_64 :: level :: foo",
        "x86_64 :: avx512f :: off",
        "x86_64 :: weirdthing :: on",
    ],
)
def test_validate_variant_fail(vprop: str, plugin) -> None:
    assert not plugin.validate_property(VariantProperty.from_str(vprop))
