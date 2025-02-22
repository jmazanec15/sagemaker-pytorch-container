# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
from __future__ import absolute_import
import os

resources_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources'))
mnist_path = os.path.join(resources_path, 'mnist')
mnist_script = os.path.join(mnist_path, 'mnist.py')
data_dir = os.path.join(mnist_path, 'data')
training_dir = os.path.join(data_dir, 'training')
dist_operations_path = os.path.join(resources_path, 'distributed_operations.py')

mnist_1d_script = os.path.join(mnist_path, 'mnist_1d.py')
model_cpu_dir = os.path.join(mnist_path, 'model_cpu')
model_cpu_1d_dir = os.path.join(model_cpu_dir, '1d')
model_gpu_dir = os.path.join(mnist_path, 'model_gpu')
model_gpu_1d_dir = os.path.join(model_gpu_dir, '1d')
