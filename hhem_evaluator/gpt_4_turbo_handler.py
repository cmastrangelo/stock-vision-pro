from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2


class GPT4Turbo:
    def __init__(self):
        PAT = '260e299f49524bf68ea4eaa8d67c0995'
        USER_ID = 'openai'
        APP_ID = 'chat-completion'
        self.MODEL_ID = 'gpt-4-turbo'
        self.MODEL_VERSION_ID = '182136408b4b4002a920fd500839f2c8'

        channel = ClarifaiChannel.get_grpc_channel()
        self.stub = service_pb2_grpc.V2Stub(channel)

        self.metadata = (('authorization', 'Key ' + PAT),)

        self.userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    def get_response(self, data, instruction_set, max_retries=3, initial_wait=2):
        RAW_TEXT = "Data to be used to make decisions:" + data + instruction_set
        post_model_outputs_response = self.stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=self.userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
                model_id=self.MODEL_ID,
                version_id=self.MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            text=resources_pb2.Text(
                                raw=RAW_TEXT
                            )
                        )
                    )
                ]
            ),
            metadata=self.metadata
        )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception(f"Post model outputs failed, status: {post_model_outputs_response.status.description}")

        # Since we have one input, one output will exist here
        output = post_model_outputs_response.outputs[0]

        return(output.data.text.raw)
