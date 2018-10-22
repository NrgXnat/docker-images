# XNAT Docker images

This is a repository of "XNAT ready" docker images which can be used with the [XNAT Container Service](https://github.com/nrgxnat/container-service).

## Writing the command(s) into an image

To be "XNAT ready" means the images have one or more [commands](https://wiki.xnat.org/display/CS/Command) formatted as a JSON list, serialized as a string, written into the images labels with the key `"org.nrg.commands"`. There is a helper script in this repository to faciliate creating these images.

1. Write the command that describes your image, and any wrappers that allow XNAT to run it with data, into a json file. I usually call these `command.json`.
2. Prepare the `Dockerfile` for the image.
3. Before you build the image, add the command(s) to the image's labels with the script:
```
[docker-images]$ ./command2label.py image-dir/command1.json image-dir/command2.json [other commands] >> image-dir/Dockerfile
```
The script will produce a `Dockerfile` instruction that looks like
```
LABEL "org.nrg.containers"="[{the contents of command1.json}, {the contents of command2.json}, ...]"
```
By redirecting that output to append to the `Dockerfile`, the proper labels will be added when building the image.

## Releasing an image

The image can be built in the normal way
```
$ docker build -t your-account/image-name:version image-dir
$ docker push your-account/image-name:version
```

Typically the images built from the contents of this repo will have the account `xnat`. Also, it is good practice to use a unique version identifier for each new image build, but to also maintain a `latest` version which gets updated to point to the most recently built version.

When you are done modifying the command and Dockerfile and other associated files for the image, merge them into the master branch and tag that commit with the image information like this:
```
$ git tag your-account_image-name_version
$ git push --tags
```

By tagging the repo in this way, we can always work backwards from an image to find the code that created that particular version of the image.
