============================================
SageMaker PyTorch Containers Build Script
============================================

Users can use docker_image_creator.py to build the Docker images with .whl files from either your local machine or the internet. To run this program, execute the command:

::

    python docker_image_creator.py  <pytorch_version> <python_version> <gpu|cpu> <binary_path>

::

binary_path can be either a URL or a path on your machine to the .whl framework binary.
To use nvidia-docker instead of docker to build the image, run the command:

::

    python docker_image_creator.py  <pytorch_version> <python_version> <gpu|cpu> <binary_path> --nvidia-docker

::

The default Docker repository the final image will be placed in is 'preprod-pytorch'. To set the repository to a custom value, run the command:

::

    python docker_image_creator.py  <pytorch_version> <python_version> <gpu|cpu> <binary_path> --final-image-repository <name>

::

The default tag the final image will have is '<framework_version>-<processor_type>-<py_version>' (i.e. 1.8.0-gpu-py2).
To customize the tag(s) set, run the command:

::

    python docker_image_creator.py  <pytorch_version> <python_version> <gpu|cpu> <binary_path> --final-image-tags <tag1> <tag2> ...

::

Here is an example for PyTorch 0.4.0 GPU:

::

    python docker_image_creator.py 0.4.0 2.7.0 gpu None
     --nvidia-docker --final-image-repository custom_repo_name --final-image-tags custom_tag1 custom_tag2

::

Notes
~~~~~

- `Only versions that have Dockerfiles in this repository can be built`
- `Python version must have 3 sections (i.e. 2.7.0 or 3.6.0)`
- `Framework version must have 3 sections (i.e. 1.1.0)`
- `Right now, the Dockerfiles do not support adding a binary, so replace binary_path with None to build with defaults`
