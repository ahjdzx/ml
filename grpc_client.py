
import argparse
import numpy as np
import sys
import cv2
import tritonclient.grpc as grpcclient
import time



url = '192.168.1.3:6001'


try:
    triton_client = grpcclient.InferenceServerClient(
        url=url,
        verbose=False,
        ssl=False,
        root_certificates=None,
        private_key=None,
        certificate_chain=None)
except Exception as e:
    print("channel creation failed: " + str(e))
    sys.exit()

model_name = "pipeline_ocr"

# Infer
inputs = []
outputs = []
inputs.append(grpcclient.InferInput('INPUT0', [1, 1], "BYTES"))

# Create the data for the two input tensors. Initialize the first
# to unique integers and the second to all ones.
img = cv2.imread('test_image.jpg')
# print(np.shape(img))
# img = cv2.resize(img, (640, 640), interpolation=cv2.INTER_CUBIC)
# cv2.imshow('', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

imgbytes = cv2.imencode('.png', img)[1]
print(len(imgbytes))
imgstring = np.array(imgbytes).tobytes()
print(len(imgstring))

input0_data = np.expand_dims([imgstring], axis=0)
# Initialize the data
inputs[0].set_data_from_numpy(input0_data)

outputs.append(grpcclient.InferRequestedOutput('OUTPUT0'))

# Test with outputs
t = time.time()

results = triton_client.infer(
    model_name=model_name,
    inputs=inputs,
    outputs=outputs,
    client_timeout=None,
    headers={'test': '1'},
    compression_algorithm=None)

tt = time.time()

print(tt - t)

statistics = triton_client.get_inference_statistics(model_name=model_name)
# print(statistics)
if len(statistics.model_stats) != 1:
    print("FAILED: Inference Statistics")
    sys.exit(1)

# Get the output arrays from the results
output0_data = results.as_numpy('OUTPUT0')
# 输出推理结果
print(output0_data.tolist().decode())
