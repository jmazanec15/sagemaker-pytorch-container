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
import numpy as np
import pytest
from test.integration import training_dir, mnist_script

from test.integration.sagemaker.estimator import PytorchTestEstimator
from test.integration.sagemaker.timeout import timeout, timeout_and_delete_endpoint


@pytest.mark.skip_gpu
def test_mnist_distributed_cpu(sagemaker_session, ecr_image, instance_type, dist_cpu_backend):
    instance_type = instance_type or 'ml.c4.xlarge'
    _test_mnist_distributed(sagemaker_session, ecr_image, instance_type, dist_cpu_backend)


@pytest.mark.skip_cpu
def test_mnist_distributed_gpu(sagemaker_session, ecr_image, instance_type, dist_gpu_backend):
    instance_type = instance_type or 'ml.p2.xlarge'
    _test_mnist_distributed(sagemaker_session, ecr_image, instance_type, dist_gpu_backend)


def _test_mnist_distributed(sagemaker_session, ecr_image, instance_type, dist_backend):
    with timeout(minutes=10):
        pytorch = PytorchTestEstimator(entry_point=mnist_script, role='SageMakerRole',
                                       train_instance_count=2, train_instance_type=instance_type,
                                       sagemaker_session=sagemaker_session, docker_image_uri=ecr_image,
                                       hyperparameters={'backend': dist_backend, 'epochs': 1})
        training_input = pytorch.sagemaker_session.upload_data(path=training_dir,
                                                               key_prefix='pytorch/mnist')
        pytorch.fit({'training': training_input})

    with timeout_and_delete_endpoint(estimator=pytorch, minutes=30):
        predictor = pytorch.deploy(initial_instance_count=1, instance_type=instance_type)

        batch_size = 100
        data = np.random.rand(batch_size, 1, 28, 28)
        output = predictor.predict(data)

        assert np.asarray(output).shape == (batch_size, 10)
