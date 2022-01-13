# pydicom_split

Wraps the [abcsFrederick/pydicom_split](https://github.com/abcsFrederick/pydicom_split) project into a container for use
with the [XNAT Container Services plugin](https://github.com/NrgXnat/container-service) and the 
[PIXI plugin](https://bitbucket.org/xnatx/pixi-plugin/src/main/). **NOTE: this is currently in development.**

## Instructions

1. First build the image:

    `docker build -t pydicom_split:latest -t pydicom_split:0.1 .`

2. In XNAT navigate to Administer -> Plugin Settings -> Container Service / Images & Commands and show all 
the hidden images. Find the `pydicom_split:0.1` image and click Add New Command. Copy the contents of 
`command_xnat_run_pydicom_split.json` into the new command modal and save.

3. Navigate to the Command Configurations tab and to enable the command at the site-wide level.

4. The command needs to be enabled at the project level. Navigate to your project, and go to Project Settings 
(found in the Actions box). From the Container Service group select Configure Commands, and enable the pydicom_split
command.

5. Before the container can split the image session a Hotel Scan Record is required. From the project homepage, in the 
actions box selec Record New Hotel Scan. Provide the Session Label of the image session to split, and enter the details 
for each hotel subject. For empty hotel positions leve the Subject ID blank.

6. After submitting the Hotel Scan Record navigate to the image session and launch the hotel splitter container. The 
hotel splitter will send the individual image sessions back to XNAT.
