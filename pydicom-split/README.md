# pydicom_split

Wraps the [abcsFrederick/pydicom_split](https://github.com/abcsFrederick/pydicom_split) project into a container for use
with the [XNAT Container Services plugin](https://github.com/NrgXnat/container-service) and the 
[PIXI plugin](https://bitbucket.org/xnatx/pixi-plugin/src/main/). **NOTE: this is currently in development.**

## Instructions

1. First either pull the image from Docker Hub or build it yourself:

    `docker pull xnat/pixi_pydicom_split:latest`

    or

    `docker build -t xnat/pixi_pydicom_split:latest .`

2. In XNAT navigate to Administer -> Plugin Settings -> Container Service / Images & Commands and select the 'New Image'
button. Enter the image name 'xnat/pixi_pydicom_split' and version tag ':latest'. Click Pull Image.

3. Navigate to the Command Configurations tab and to enable the command at the site-wide level.

4. The command needs to be enabled at the project level. Navigate to your project, and go to Project Settings 
(found in the Actions box). From the Container Service group select Configure Commands, and enable the pydicom_split
commands.

5. Before the container can split the image session a Hotel Scan Record is required. From the project homepage, in the 
actions box select 'Record Preclinical Data' -> 'Record New Hotel Scan'. Provide the Session Label of the image session to 
split, and enter the details for each hotel subject. Click Submit.

6. After submitting the Hotel Scan Record launch the hotel splitter container by selecting 'Run Containers' -> 
'Scan Record Splitter'. The hotel splitter will split hotel image session and send the individual image sessions back to
XNAT.
