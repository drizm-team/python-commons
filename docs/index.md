# Drizm Python Commons

<p align="center">
    <a href="https://badge.fury.io/py/drizm-commons">
        <img 
        src="https://badge.fury.io/py/drizm-commons.svg" 
        alt="PyPI version" height="18"
        >
    </a>
    <a href="https://github.com/psf/black">
        <img
        src="https://img.shields.io/badge/code%20style-black-000000.svg"
        alt="Code Style" height="18"
        >
    </a>
</p>

This package contains shared code used by
the Drizm organizations development team.  

It is not intended for public usage,
but you may still download,
redistribute or modify it to your liking.

**Author:**  
Ben "ThaRising" Koch

## Requirements

Python **^3.8.X** supported.

**Debian 9+** and **Ubuntu 18.04+** for Linux,
as well as **Windows 10 1909+**,
are tested and supported.

Other OS are still most likely supported,
but were not explicitly tested.

## Features

This project implements utilities for a very
broad range of use-cases and packages.

As such, fully installing everything may not
be the route you want to go.

The following features are supported:

| Featureset                 | Module-Name | Extra-Name  |
| :------------------------- | :---------- | :---------- |
| SQLAlchemy Utilities       | *sqla*      | *sqla*      |
| GoogleCloudPlatform Extras | *google*    | *google*    |
| General Utilities          | -           | -           |
| Testing Utilities          | -           | -           |

All feature-sets without an extra extra-name,
are included in the minimal installation.

## Installation

### Minimal Installation

````commandline
pip install drizm-commons
````

This will only inlcude the 
[testing](testing.md) and
[utils](utils.md) subpackages.

### Installation with Extras

Install SQLAlchemy features:  
````commandline
pip install drizm-commons[sqla]
````

Install Google-Cloud utils:  
````commandline
pip install drizm-commons[google]
````

### Complete Installation

Complete installation (everything above):  
````commandline
pip install drizm-commons[all]
````

### Importing the Package

Once installed, you can import
the package like so:
````python
import drizm_commons
````
