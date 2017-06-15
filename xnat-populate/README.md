# xnat-populate

Wraps the [XNAT Populate](https://bitbucket.org/xnatdev/xnat_populate) project up in a minimal container. NOTE: this should only be used in dev environments.

Providing the user, password, and site URL are not necessary, since they are handled by the Container Service. The only thing required is a list of project IDs, separated by commas. After POSTing the command.json, you can launch it by doing a POST to:

```
$ /xapi/wrappers/${wrapperId}/launch?project_list=${projects}
```

So, one example could be:

```
$ /xapi/wrappers/1/launch?project_list=Angio_XA,Behavior_DB
```

Currently, the more advanced options of XNAT Populate such as specifying site configuration or exporting from XNAT are not yet supported in the Docker build.

