# Changelog

### 0.1.1

- Added SQLAlchemy JSON Encoder
- Fixed bugs related to the Introspection
API
- Added table registry
- Added additional utilities

### 0.1.2

- Added get_root_path and recursive delete
Path utilities
- Fixed various bugs

### 0.2.0

- Added full test suite
- Added testing tools
- Revamped introspection API
- Provided additional overrides for the
SQL connection adapter

### 0.2.1

- Added support for datetime JSON
encoding

### 0.2.2

- Improved in-code documentation
- Integrated additional utils from
drizm-django-commons

### 0.3.0

- Added introspection capabilities 
for property and SQLAlchemy's
hybrid_property
- SQLAEncoder now respects property
and hybrid_property on SQLA declarative
instances
- Additional customizability hooks
for custom fields or data handling
- Support for JSON-Encoding table
instances
- Added SQLA as optional dependency
- Added additional testing utilities

### 0.3.1

- Improved code documentation
- Added docs
- Added memoize function decorator
to cache last previously passed
function parameter

### 0.3.2

- Fixed issue with introspection API
picking up validation methods

### 0.3.3

- Added additional tests and bugfixes

### 0.3.4

- Added support for comments and
special character parsing to Tfvars

### 0.4.0

- Added method to force obtain
GoogleCloudPlatform Id-Tokens

### 0.4.1

- Added function to convert
CamelCase to snake_case

### 0.4.2

- Added TestStorageBucket
- Updated docs
- Added camelCase to snake_case
name converter

## 0.5.0

The most major update thus far.

It includes a complete restructuring
of the package, as well as full
blown documentation.

Additionally, the test coverage
is now much higher and more manual
testing has been done to ensure that
everything works as expected in as many
scenarios as possible.

Additions:

- drizm_commons.utils.type.IterableKeysDictionary
- drizm_commons.utils.decorators.resolve_super_auto_resolution
- drizm_commons.testing.faker.*
- drizm_commons.conversion.*
- drizm_commons.biased.*

Improvements:

- get_absolute_root_path() now
  supports more ways of determining
  the project root correctly and is
  now much more accurate
- AttrDict now automatically converts
  '-' to '_' in keys
- Multiple improvements to the truthiness
  functions
