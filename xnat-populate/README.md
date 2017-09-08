# xnat-populate

Wraps the [XNAT Populate](https://bitbucket.org/xnatdev/xnat_populate) project up in a container for use with the [XNAT Container Services plugin](https://github.com/NrgXnat/container-service). NOTE: this should only be used in dev environments.

Providing the user, password, and site URL are not necessary, since they are handled by the Container Service. Since the Dockerfiles contain the commands already, you should not need to set them up. There are two Dockerfiles, one in "cached_data", and one in "uncached". The images from both files do cache the dependencies needed to run the groovy project. The difference between the two Dockerfiles is that the "cached_data" version additionally downloads all of the XNAT Populate data. The tradeoff is that executing the command can then skip the download step, but the generated image is very large. The currently available command is:

## xnat_populate ##

The command runs XNAT Populate with minimal parameters. The only thing required from the user is a comma-separated list of project IDs to populate provided to the `project_list` variable (alternatively, the file name of one of the standard populate data files can be used). Usage then looks like:

```
$ /xapi/wrappers/${wrapperId}/launch?project_list=${projects}
```

So, one example could be:

```
$ /xapi/wrappers/1/launch?project_list=Angio_XA,Behavior_DB
```

Additionally, two optional parameters can be used. Specifying a value for `delay` in milliseconds will cause XNAT Populate to pause that long between session uploads, and specifying a file name for `config` will cause XNAT Populate to configure this XNAT according to the YAML file separated. A full usage example could therefore be:

```
$ /xapi/wrappers/1/launch?project_list=Angio_XA,Behavior_DB&delay=3000&config=internalDevConfig.yaml
```
