# provider-variant-x86-64

This is a plugin for the proposed [wheel variants implementation](
https://github.com/wheelnext/pep_xxx_wheel_variants) that provides
properties specific to x86-64 CPUs.

## Usage

Namespace: `x86_64`

Plugin API: `provider_variant_x86_64.plugin:X8664Plugin`

Example use in `pyproject.toml`:

```toml
[variant.providers.x86_64]
requires = ["provider-variant-x86-64 >=0.0.1,<1"]
plugin-api = "provider_variant_x86_64.plugin:X8664Plugin"
```

## Provided properties

To obtain the full list of properties supported by a given plugin
version, use:

```sh
variantlib plugins -p provider_variant_x86_64.plugin:X8664Plugin get-all-configs
```

To obtain the full list of properties compatible with your system, use:

```sh
variantlib plugins -p provider_variant_x86_64.plugin:X8664Plugin get-supported-configs
```

### x86_64 :: level

Values: `v1`, `v2`...

Specifies the targeted [microarchitecture level](
https://en.wikipedia.org/wiki/X86-64#Microarchitecture_levels).
The plugin automatically adds appropriate `-march=` value to `CFLAGS`.
The resulting wheel will be incompatible with CPUs below the specified
microarchitecture level.

### x86_64 :: &lt;extension&gt;

Feature names: `aes`, `avx2`, `sse4_1`...

Values: `on`

Specifies that the built wheel uses the specific CPU extension.
The plugin does not emit any compiler flags at the moment.
The resulting wheel will be incompatible with CPUs that do not implement
the specific extension.

Note that while these properties are independent of microarchitecture
levels, there is little purpose in specifying them if the wheel already
specifies a microarchitecture level requiring a specific extension.

These properties should only be used when the relevant intrinsics are
used unconditionally. If the code using them uses runtime detection,
they should not be specified, as they will prevent installing the wheel
on systems where the extension is not available (yet the code would work
fine, disabling the code in question).
