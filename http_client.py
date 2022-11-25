import requests
import cv2
import numpy as np
import tritonclient.http as httpclient


if __name__ == "__main__":
    triton_client = httpclient.InferenceServerClient(url='192.168.1.3:6000')

    inputs = []
    inputs.append(httpclient.InferInput('INPUT0', [1, 1], "BYTES"))
    img = cv2.imread('test_image.jpg')
    imgbytes = cv2.imencode('.png', img)[1]
    imgstring = np.array(imgbytes).tobytes()
    input0_data = np.expand_dims([imgstring], axis=0)
    inputs[0].set_data_from_numpy(input0_data)
    outputs = []
    outputs.append(httpclient.InferRequestedOutput('OUTPUT0', binary_data=False))

    results = triton_client.infer('pipeline_ocr', inputs=inputs, outputs=outputs)

    result = results.as_numpy("OUTPUT0")
    print(result)
