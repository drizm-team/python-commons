# Drizm Python Commons
[![PyPI version](https://badge.fury.io/py/drizm-commons.svg)](https://badge.fury.io/py/drizm-commons)  

This package contains shared code used by
the Drizm organizations development team.  

It is not intended for public usage,
but you may still download,
redistribute or modify it to your liking.

## Requirements

Python 3.8 supported.

## Installation

Basic Install (utils only):  
``pip install drizm-commons``

Install SQLAlchemy features:  
``pip install drizm-commons[sqla]``  
Install Google-Cloud utils:  
``pip install drizm-commons[google]``  
Install everything:  
``pip install drizm-commons[sqla,google]``

Import as:  
*import drizm_commons*

## Features

- GCP Utilities
- Testing Utilities
- Extras for working with Terraform
- Basic Introspector for various
SQLAlchemy classes

## Google Cloud Tools

**import drizm_commons.google**

### force_obtain_id_token()

Can be used to obtain an OIDC-Token for authenticating
against GoogleCloud services.

````python
from drizm_commons.google import force_obtain_id_token
from google.oauth2 import service_account


auth = service_account.IDTokenCredentials.from_service_account_file(
    "/path/to/svc.json",
    target_audience="https://example.com/"
)
token = force_obtain_id_token(auth)
# Returns an access token with the structure 'ey....'
````

### TestStorageBucket

Used to generate a V4 Signed-URL for use with GCS.  
This can also be done using the GoogleCloudStorage

````python
from drizm_commons.google import TestStorageBucket
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    "path/to/svc.json"
)
test_bucket = TestStorageBucket(
    project_id="your-project-id",
    credentials=credentials
)
test_bucket.create()

# ... do whatever you need to test ...

test_bucket.destroy()
````

## Utilities

**Convinience Functions:**  
````python
from drizm_commons.utils import *


# Check whether function name is dunder
is_dunder("__name__")  # True

# Check if a given string is a valid UUIDv4
uuid4_is_valid("myvalue")  # False

# Check if a URL is valid and the contents URL-Safe
url_is_http("https://myapp.com/")  # True

# Get the current applications root path
Path(get_application_root())
````

**Path with extra features:**
````python
from drizm_commons.utils import Path

# Recursively delete a folder
path = Path(__file__).parent
path.rmdir(recursive=True)
````

**Cache last passed parameter:**
````python
from drizm_commons.utils import memoize


@memoize
def foo(a):
    return a


foo(3)  # 3
foo()  # 3
````

## SQLA Introspection

````python
from drizm_commons.inspect import SQLAIntrospector


table = SQLAIntrospector(my_table_instance)

""" Attributes """
table.tablename  # get the name of the table
table.classname  # get the classname of the declarative instance
table.columns  # get all SQLA fields of the class
table.column_attrs  # get all SQLA fields + property and hybrid_property of the class
````

## Changelog

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
