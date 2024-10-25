######################################################################################################
# In this section, we set the user authentication, user and app ID, model details, and the text prompt
# we want as an input. Change these strings to run your own example.
######################################################################################################

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import streamlit as st

# Your PAT (Personal Access Token) can be found in the portal under Authentication
PAT = st.secrets.PAT
# Specify the correct user_id/app_id pairings
USER_ID = st.secrets.USER_ID
APP_ID = st.secrets.APP_ID
# Change this to the model/workflow ID you want to use
WORKFLOW_ID = 'Llama2TutorialWorkflow'

############################################################################
# YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
############################################################################

def get_response(prompt):
    # Set up the Clarifai API channel and stubs
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    # Set up the metadata for authentication
    metadata = (('authorization', 'Key ' + PAT),)

    # Define user data with user and app IDs
    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    response_text = ""  # Variable to store model response

    # Call the workflow with the prompt input
    post_workflow_results_response = stub.PostWorkflowResults(
        service_pb2.PostWorkflowResultsRequest(
            user_app_id=userDataObject,
            workflow_id=WORKFLOW_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw=prompt  # Passing prompt directly as text
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )

    # Check for successful response
    if post_workflow_results_response.status.code != status_code_pb2.SUCCESS:
        print("Error:", post_workflow_results_response.status.description)
        return response_text  # Return empty if unsuccessful

    # Process and print the response output from the model
    results = post_workflow_results_response.results[0]
    for output in results.outputs:
        model = output.model
        print("Predicted concepts for the model `%s`" % model.id)
        for concept in output.data.concepts:
            print("\t%s %.2f" % (concept.name, concept.value))
        
        # Concatenate each output text to response_text
        response_text += output.data.text.raw + "\n"

    print(response_text)  # Optionally print the full response
    return response_text
