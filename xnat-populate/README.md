# xnat-populate

Wraps the [XNAT Populate](https://bitbucket.org/xnatdev/xnat_populate) project up in a minimal container. NOTE: this should only be used in dev environments.

Providing the user, password, and site URL are not necessary, since they are handled by the Container Service. Since the Dockerfile contains the commands already, you should not need to set them up. Currently available commands are:

## simple_populate ##

The command runs XNAT Populate with minimal parameters. The only thing required from the user is a comma-separated list of project IDs to populate provided to the project_list variable. Usage then looks like:

```
$ /xapi/wrappers/${wrapperId}/launch?project_list=${projects}
```

So, one example could be:

```
$ /xapi/wrappers/1/launch?project_list=Angio_XA,Behavior_DB
```

## populate_with_site_config ##

This command is the same as the previous one, except that it adds the config_file parameter to add some site configuration from any of the standard configuration YAML files provided with XNAT Populate. Usage then looks like:

```
$ /xapi/wrappers/${wrapperId}/launch?project_list=${projects}&config_file=${file_name}
```

So, one example could be:

```
$ /xapi/wrappers/2/launch?project_list=Angio_XA,Behavior_DB&config_file=demoConfig.yaml
```
