## 📜 Changelog

Here we track the changes from release to release.

### 1.2.1

This release updates [Sickbay](https://pypi.org/project/mcl.sickbay/) to 1.2.1.


### 1.2.0

This release updates [Sickbay](https://pypi.org/project/mcl.sickbay/) to 1.2.0.


### 1.1.0

This release updates [Sickbay](https://pypi.org/project/mcl.sickbay/) to 1.1.0 and also removes the last vestiges of [zc.buildout](https://www.buildout.org/).


### 1.0.2

This release updates [Sickbay](https://pypi.org/project/mcl.sickbay/) to 1.0.2.


### 1.0.1

This release updates [Sickbay](https://pypi.org/project/mcl.sickbay/) to 1.0.1 and is used in the v2 API endpoint.


### 1.0.0

This release adds a handler for `/` which apparently is required for [JPL](https://www.jpl.nasa.gov/) to complete its security scan.


### 0.0.6

This release upgrades [Sickbay](https://pypi.org/project/mcl.sickbay/) to 1.0.0.


### 0.0.5

This release upgrades [Sickbay](https://pypi.org/project/mcl.sickbay/) to 0.0.10.


### 0.0.4

This release upgrades [Sickbay](https://pypi.org/project/mcl.sickbay/) to 0.0.9.


### 0.0.3

This release upgrades [Sickbay](https://pypi.org/project/mcl.sickbay/) to 0.0.7; see issue https://github.com/MCLConsortium/mcl.infirmary/issues/2.


### 0.0.2

-   [Issue 1](https://github.com/MCLConsortium/mcl.infirmary/issues/1)
    -   Adds version (and [Sickbay](https://pypi.org/project/mcl.sickbay/) version) to the `/ping` endpoint
    -   Add `--version` command-line option
    -   Announces the version to the `info` log at start-up
-   Updates [mcl.sickbay](https://pypi.org/project/mcl.sickbay/) dependency to 0.0.6
    -   Takes advantage of new consortium and protocol ID data


### 0.0.1

In this release, we added the changelog! 🤯

We also pin to version `mcl.sickbay-0.0.5`. For some reason, we can't do a `python3 setup.py install` without it pinned inside the Docker image creation 🤷‍♀️
