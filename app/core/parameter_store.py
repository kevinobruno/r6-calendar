import boto3


class ParameterStore():
    def __init__(self):
        self._client = boto3.client('ssm')
        self._base = 'r6-calendar'

    def get(self, name):
        env_var_name = f'/{self._base}/{name}'
        parameter = self._client.get_parameter(Name=env_var_name, WithDecryption=True)
        return parameter['Parameter']['Value']
