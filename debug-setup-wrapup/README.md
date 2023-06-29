Debug with setup and wrapup
===========================

A single debug command that uses a setup command and a wrapup command. 

At each stage (setup, main, and wrapup) the container will log the contents of `/input` to stdout.
It will also create a file in `/output` called `<stage>-was-here` named for its stage.

After setup (i.e. main and wrapup) the container will also copy the previous `<stage>-was-here` file or files
from `/input` to `/output`.

# Installation
Navigate to Container Service admin UI: Administer > Plugin Settings, then Images and Commands tab.
Click the "New Command" button. 
Copy and paste one of the command jsons from this repo. Then do it two more times.
Sorry this is bad!
