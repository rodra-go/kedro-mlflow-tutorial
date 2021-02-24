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

from erc.pipelines.data_science.nodes import (
    estimator,
    train_svm_regressor,
    evaluate_svm_regressor,
    train_svm_classifier,
    evaluate_svm_classifier
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=estimator,
                inputs=[
                    "transformed_sgs_dataset",
                    "params:estimator.sgs_session_id",
                    "params:estimator.sgs_env_cond_id",
                    "params:estimator.expected_tp",
                    "params:estimator.target_columns",
                    "params:estimator.delta",
                    "params:estimator.repetitions",
                    "params:estimator.window_size",
                ],
                outputs=[
                    "estimator_metrics",
                    "estimator_tp_x_psd_figure",
                    "estimator_tp_x_figure",
                    "estimator_tp_y_psd_figure",
                    "estimator_tp_y_figure"
                ],
                name="estimator",
                tags=["data_science","estimator"],
            ),
            node(
                func=train_svm_regressor,
                inputs=[
                    "regressor_x_train",
                    "regressor_tp_x_train",
                    "regressor_tp_y_train",
                    "params:regressor.svr.hyperp.kernel",
                    "params:regressor.svr.hyperp.gamma",
                ],
                outputs=[
                    "regressor_tp_x_model",
                    "regressor_tp_y_model",
                    "regressor_model_training_metrics",
                ],
                name="svm_regressor_training",
                tags=["data_science","regressor"],
            ),
            node(
                func=evaluate_svm_regressor,
                inputs=[
                    "regressor_tp_x_model",
                    "regressor_tp_y_model",
                    "regressor_x_scaler",
                    "regressor_tp_x_scaler",
                    "regressor_tp_y_scaler",
                    "regressor_x_test",
                    "regressor_tp_x_test",
                    "regressor_tp_y_test",
                ],
                outputs="regressor_model_testing_metrics",
                name="svm_regressor_testing",
                tags=["data_science","regressor"],
            ),
            node(
                func=train_svm_classifier,
                inputs=[
                    "classifier_x_train",
                    "classifier_y_train",
                    "params:classifier.svc.hyperp.kernel",
                    "params:classifier.svc.hyperp.gamma",
                ],
                outputs=[
                    "classifier_model",
                    "classifier_model_training_metrics",
                ],
                name="svm_classifier_training",
                tags=["data_science","classifier"],
            ),
            node(
                func=evaluate_svm_classifier,
                inputs=[
                    "classifier_model",
                    "classifier_x_test",
                    "classifier_y_test",
                ],
                outputs="classifier_model_testing_metrics",
                name="svm_classifier_testing",
                tags=["data_science","classifier"],
            )
        ]
    )
