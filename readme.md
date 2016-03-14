# Azure APIm Deployment Utils

## Introduction

In order to automate deployment to and from Azure API Management instances, we needed some kind of tooling to accomplish this. In many cases, the Azure Powershell Cmdlets will help you doing things, but in some cases, they just don't go far enough, and/or you want to deploy from a Linux/Mac OS X build agent/client.

We wanted to be able to accomplish the following things:

* Extract configuration from an API Management instance as far as possible, using the REST API and/or git Repository integration
* Push configurations to other APIm instances, using both the REST API and the git repository.

The python scripts at hand can do these things, mostly using the git integration.

**Discaimer**: The scripts were developed on Mac OS X, and will most likely work on Linux and Windows, too, but have not (yet) been tested to do so.

### How does this work?

This is the principal idea how the scripts are intended to work:

![Deployment Paths](doc/deployment_path.png)

In this picture you see three (point being: two or more) different instances of API Management which reflect the different stages of development of your API Management solution.

An Azure API Management instance configuration consists of a lot of information, of which most is retrievable using the [`git` integration](https://azure.microsoft.com/en-us/updates/manage-your-api-management-service-instances-by-using-git/), but not all information is contained in the repository. Namely the following things are not included:

* Client Certificates for use for Mutual SSL connections to the backend
* Properties for parametrizing policy definitions

This means any deployment script needs to take care of these things in addition to just pushing the git configuration to a different instance. Fortunately, there is a REST API of Azure API Management which lets you do that, and this is also addressed by the scripts.

Additionally, all CRM content is (unfortunately) not contained in the git repository, but that part is **not** covered by the scripts (as the content is not available "from the outside").

#### What's in this package?

To get the expectations straight for these scripts: The scripts are intended to **enable** you to do automatic deployments to and from Azure API Management instances, but they can only provide a means for you to do this. Depending on your deployment scenarios, you will need different lego bricks to build up your pipelines.

In the following sections I will describe the deployment pipeline we have chosen you use, but your mileage may vary largely.

In case you have use cases you think are missing/the scripts do not reflect this, please open an issue so that we can discuss possible solutions.

#### Development principles

...

#### Development cycle

...

### Consequences of automation

When deciding to automate the deployment of API definitions to Azure API Management, this will have some effects on how you need to design/implement policies. The following section describe some typical problems you encounter and the workarounds and/or patterns you can apply to achieve what you need.

#### Making the service URL configurable

A major pain point with the API definitions in Azure API Management is that it is not - out of the box - possible to parametrize the `serviceUrl` of an API (also known as the service backend URL). One would expect it to be possible to use a property to supply the URL, but unfortunately, this is not possible (using ``{{MyApiBackendUrl}}` is rejected for not being a proper URL).

The workaround for this is to use the `<set-backend-service>` policy on an API level, and there make use of a property.

**Example**:
```xml
<policies>
	<inbound>
		<base />
		<set-backend-service base-url="{{MyApiBackendUrl}}" />
	</inbound>
	<backend>
		<base />
	</backend>
	<outbound>
		<base />
	</outbound>
	<on-error>
		<base />
	</on-error>
</policies>
```

**Remember**: No hard coded URLs, user names and/or passwords inside your `git` repository, otherwise you'll be unhappy. All moving parts in certificates and properties only!

#### Automated updates of API definitions via Swagger

In order to update an API via its Swagger definition using the REST API (as opposed to the Web UI), it is necessary to know the *aid* (API ID) of the API to update. Finding this id is either a matter of pattern matching, or you need to define a unique ID which is both present in the APIm instance and on your own side.

To solve this problem, the scripts at hand chose to "abuse" the `serviceUrl` (see also above) to map the API to a Swagger definition. See section on the [`swaggerfiles.json`](#swaggerfiles) configuration file properties. This issue is described in more depth there.

## Prerequisites

In order to run the scripts, you will need the following prerequisites installed on your system:

* Python 2.7.x
* PIP
* The Python `requests` library: [Installation Guide](http://docs.python-requests.org/en/master/user/install/)
* The Python `gitpython` library: [Installation Guide](http://gitpython.readthedocs.org/en/stable/intro.html)
* `git` (available from the command line)

### On `pip` packages

As I haven't been writing python scripts for more than a couple of days, I have not yet found out how to create my own "eggs" and/or `pip` packages/applications. This will hopefully follow in due time.

# Usage

Depending on the script you are using, the deployment scripts expect information from files residing in the same directory (referred to as the *configuration directory*). 

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

<a name="swaggerfiles"></a>
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
