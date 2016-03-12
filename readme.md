# Azure APIm Deployment Utils

## Introduction

In order to automate deployment to and from Azure API Management instances, we needed some kind of tooling to accomplish this. In many cases, the Azure Powershell Cmdlets will help you doing things, but in some cases, they just don't go far enough, and/or you want to deploy from a Linux/Mac OS X build agent/client.

We wanted to be able to accomplish the following things:

* Extract configuration from an API Management instance as far as possible, using the REST API and/or git Repository integration
* Push configurations to other APIm instances, using both the REST API and the git repository.

The python and shell scripts at hand can do these things, mostly using the git integration. They are intended for use in a Linux or Mac OS X environment; possibly they will work using git bash/cygwin on Windows, too, but that's not been thoroughly tested.

## Prerequisites

In order to run the scripts, you will need the following prerequisites installed on your system:

* sh (shell scripts)
* Python 2.7.x
* PIP
* The Python `requests` library: [Installation Guide](http://docs.python-requests.org/en/master/user/install/)
* The Python `gitpython' library: [Installation Guide](http://gitpython.readthedocs.org/en/stable/intro.html)
* git (available from the command line)

### On `pip` packaes

As I haven't been writing python scripts for more than a couple of days, I have not yet found out how to create my own "eggs" and/or `pip` packages/applications. This will hopefully follow in due time.

# Usage

The following sections describe the callable python scripts; I hope I will find time to describe the actual implementation in more detail, too, but for now, this will have to do.

## Configuration directory structure

You can find a sample configuration repository inside the `sample-repo` directory. The following files are considered when dealing with an Azure API Management configuration:

* `certificates.json`: This file contains the certificates meta information which gives information on which certificates for use as client certificates when calling backend service are to be used. These certificates are subsequently to be used in authentication policies. See the sample file for a description of the file format.
* `instances.json`: A file containing the `id`, `primaryKey` and other information on the Azure APIm instance to work with. It makes sense to get this information from environment variables, e.g. for use with build environments (which can pass information via environment variables).
* `properties.json`: Properties to update in the target APIm instances. See the file for the syntax. Properties can be used in most policy definitions to get a parametrized behaviour. Typical properties may be e.g. backend URLs (used in `set-backend-service` policies), user names or passwords.
* `swaggerfiles.json`: Used when updating APIs via swagger files which are generated and/or supplied from a backend service deployment.

### Config file `certificates.json`

To be written.

### Config file `properties.json`

To be written.

### Config file `instances.json`

To be written.

### Config file `swaggerfiles.json`

To be written.

## Updating an APIm instance

```
$ python apim_update.py <config dir>
```

...

(This already works)

## Extracting a configuration ZIP file

```
$ python apim_extract.py <config dir> <target zip file>
```
...

(This already works)

## Deploying a configuration ZIP file (to a different APIm instance)

```
$ python apim_deploy.py <source config zip>
```

Things which are confusing:

* The entire configuration is taken from the ZIP file, also the `instances.json`; normally you would parametrize this using environment variables, and via that be able to deploy to a different instance.

### Special case deleted 'loggers'

... can't be removed in the same step as they are removed from the policies. Two-step deployment (call it a bug of APIm if you want).

### Special case deleted properties

... can't be removed in the same step as they are removed from the policies. Two-step deployment (call it a bug of APIm if you want).

## Extracting Properties

```
$ python apim_extract_properties.py <config dir>
```


# Appendix

## Further Reading

Links to the Azure APIm documentation:

* ...
