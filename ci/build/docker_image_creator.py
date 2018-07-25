""" Script to create Sagemaker PyTorch Docker images

    Usage:
        python docker_image_creator.py binary_path gpu|cpu pytorch_version python_version
"""
import argparse
import glob
import os
import requests
import shutil
import subprocess

def build_docker_image(framework_version, python_version, processor, binary_path, final_image_repository,
                        final_image_tags, docker, main_directory_path):
    """ Function builds TF docker image

    Args:
        framework_version (str): tensorflow version i.e 1.6.0
        python_version (str): (i.e. 3.6.5 or 2.7.4)
        processor (str): gpu or cpu
        binary_path (str): path to where the binary is.
        final_image_repository (str): name of final repo.
        final_image_tags (list(str)): list of tag names for final image
        docker (str): either nvidia-docker or docker
        main_directory_path (str):  absolute path to where the sagemaker-tensorflow-repo
    """
    # Initialize commonly used variables
    py_v = 'py{}'.format(python_version.split('.')[0]) # i.e. py2
    base_docker_path = os.path.join(main_directory_path, 'docker', framework_version, 'base')
    final_docker_path = os.path.join(main_directory_path, 'docker', framework_version, 'final')

    # Get binary file
    if binary_path != 'None':
        print('Getting binary...')
        if os.path.isfile(binary_path):
            binary_filename = os.path.basename(binary_path)
            shutil.copyfile(binary_path, os.path.join(final_docker_path, binary_filename))
        else:
            binary_filename = binary_path.split('/')[-1]
            binary_response = requests.get(binary_path)
            with open(os.path.join(final_docker_path, binary_filename), 'wb') as binary_file:
                binary_file.write(binary_response.content)

    # Build base image
    print('Building base image...')
    image_name = 'pytorch-base:{}-{}-{}'.format(framework_version, processor,  py_v)
    subprocess.call([docker, 'build', '-t', image_name, '--build-arg', 'py_version={}'.format(py_v[-1]),
                     '-f', 'Dockerfile.{}'.format(processor), '.'], cwd=base_docker_path)

    #  Build final image
    print('Building final image...')
    subprocess.call(['python', 'setup.py', 'bdist_wheel'], cwd='{}'.format(main_directory_path))
    final_command_list = [docker, 'build']
    for tag in final_image_tags:
        final_command_list.append('-t')
        final_command_list.append('{}:{}'.format(final_image_repository, tag))

    if binary_path != 'None':
        final_command_list.extend(['--build-arg', 'framework_installable={}'.format(binary_filename)])

    final_command_list.extend(['--build-arg', 'py_version={}'.format(py_v[-1]), '-f',
                               os.path.join(final_docker_path, 'Dockerfile.{}'.format(processor)), '.'])

    subprocess.call(final_command_list, cwd='{}'.format(main_directory_path))

def main():
    # Parse command line options
    parser = argparse.ArgumentParser(description='Build Sagemaker PyTorch Docker Images')
    parser.add_argument('framework_version', help='Framework version (i.e. 0.4.0)')
    parser.add_argument('python_version', help='Python version to be used (i.e. 2.7.0)')
    parser.add_argument('processor_type', choices=['cpu', 'gpu'], help='gpu if you would like to use GPUs or cpu')
    parser.add_argument('binary_path', help='Enter None')
    parser.add_argument('--nvidia-docker', action='store_true', help='Enables nvidia-docker usage over docker')
    parser.add_argument('--final-image-repository', default='preprod-tensorflow',
                        help='Name of final docker repo the image is stored in')
    parser.add_argument('--final-image-tags', default=[], nargs='+', help='List of tag names for final image')
    args = parser.parse_args()

    # Arguments used in build functions
    docker = 'nvidia-docker' if args.nvidia_docker else 'docker'
    main_directory_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..')
    if args.final_image_tags:
        final_image_tags = args.final_image_tags
    else:
        final_image_tags = ['{}-{}-py{}'.format(args.framework_version, args.processor_type, args.python_version[0])]

    # Build the image
    build_docker_image(args.framework_version, args.python_version, args.processor_type, args.binary_path,
                        args.final_image_repository, final_image_tags, docker, main_directory_path)

if __name__ == '__main__':
    main()
