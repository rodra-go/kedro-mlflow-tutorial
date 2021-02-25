# Copyright 2020 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

Delete this when you start working on your own Kedro project.
"""

from kedro.pipeline import Pipeline, node

from kedro_mlflow_tutorial.pipelines.data_engineering.nodes import (
    transform_coordinates,
    generate_feature_data,
    generate_training_data,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=transform_positions,
                inputs="sgs_dataset",
                outputs="transformed_sgs_dataset",
                name="transform_positions",
                tags="data_engineering"
            ),
            node(
                func=generate_feature_data,
                inputs=[
                    "transformed_sgs_dataset",
                    "params:estimator.expected_tp",
                    "params:estimator.target_column",
                    "params:estimator.delta",
                    "params:estimator.repetitions",
                    "params:estimator.window_size",
                ],
                outputs="feature_dataset",
                name="generate_feature_data",
                tags="data_engineering"
            ),

            node(
                func=generate_training_data,
                inputs=[
                    "feature_dataset",
                    "params:estimator.target_column",
                    "params:regressor.test_size",
                    "params:regressor.valid_size",
                    "params:regressor.shuffle",
                ],
                outputs= [
                    "x_train",
                    "x_valid",
                    "x_test",
                    "x_scaler",
                    "y_train",
                    "y_valid",
                    "y_test",
                    "y_scaler",
                ],
                name="generate_training_data",
                tags=["data_engineering"]
            ),
        ]
    )
