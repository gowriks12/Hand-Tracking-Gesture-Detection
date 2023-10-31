import numpy as np
import boto3
import sagemaker
import json
import io
import pandas as pd

def get_prediction(input_data):
    # Set your AWS region and SageMaker endpoint name

    aws_region = 'us-east-2'
    endpoint_name = 'Custom-sklearn-model-2023-10-30-17-28-33'

    # Initialize a SageMaker runtime client
    sagemaker_runtime = boto3.client('sagemaker-runtime', region_name=aws_region)

    payload = io.StringIO()
    data2 = np.array(input_data).reshape(1, -1)
    # input_data = input_data
    input_data = pd.DataFrame(data2)
    input_data.to_csv(payload, header=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], index=None)

    try:
        # Send a request to the SageMaker endpoint for prediction
        response = sagemaker_runtime.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType='text/csv',
            Body=payload.getvalue(),
        )

        # Parse the response
        result = response['Body'].read().decode('utf-8')
        result = json.loads(result)

        # Print or use the prediction result
        print("Prediction:", result[1])
        return result[1]

    except Exception as e:
        print("Error:", e)
