import number

import numpy as np

from onnx_tf.common import exception
from onnx_tf.handlers.frontend_handler import FrontendHandler
from onnx_tf.handlers.handler import onnx_op
from onnx_tf.handlers.handler import tf_op


@onnx_op("ConstantFill")
@tf_op("Fill")
class Fill(FrontendHandler):

  @classmethod
  def args_check(cls, node, **kwargs):
    output_shape = node.attr["_output_shapes"][0]
    for dim_size in output_shape:
      assert isinstance(dim_size, numbers.Number)
    if node.inputs[1] not in kwargs["consts"]:
      exception.CONST_NOT_FOUND_EXCEPT(node.inputs[1], node.op_type)

  @classmethod
  def version_1(cls, node, **kwargs):
    value = float(np.asscalar(kwargs["consts"][node.inputs[1]]))
    return cls.make_node_from_tf_node(
        node, [node.inputs[0]], input_as_shape=1, value=value)

  @classmethod
  def version_9(cls, node, **kwargs):
    value = float(np.asscalar(kwargs["consts"][node.inputs[1]]))
    outputs = cls.get_outputs_names(node)
    return cls.make_node(
        "ConstantLike", node, outputs, shape=output_shape, value=value)
