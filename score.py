# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
import logging
import os
import pickle
import numpy as np
import pandas as pd
from sklearn.externals import joblib

import azureml.automl.core
from azureml.automl.core.shared import logging_utilities, log_server
from azureml.telemetry import INSTRUMENTATION_KEY

from inference_schema.schema_decorators import input_schema, output_schema
from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType
from inference_schema.parameter_types.pandas_parameter_type import PandasParameterType


input_sample = pd.DataFrame({"CodigoCliente": pd.Series(["1"], dtype="int64"), "Titulo": pd.Series(["Sra."], dtype="object"), "PrimeiroNome": pd.Series(["Fernanda"], dtype="object"), "UltimoNome": pd.Series(["Camargo"], dtype="object"), "Idade": pd.Series(["32"], dtype="int64"), "Sexo": pd.Series(["Feminino"], dtype="object"), "Endereco": pd.Series(["Rua Paulo Suplicy, 376"], dtype="object"), "Cidade": pd.Series(["S\u00e3o Paulo"], dtype="object"), "UF": pd.Series(["SP"], dtype="object"), "UFCompleto": pd.Series(["S\u00e3o Paulo"], dtype="object"), "CEP": pd.Series(["54210-520"], dtype="object"), "Pais": pd.Series(["BR"], dtype="object"), "PaisCompleto": pd.Series(["Brazil"], dtype="object"), "Email": pd.Series(["fecamargo@gmail.com"], dtype="object"), "RendaMensal": pd.Series(["8000"], dtype="int64"), "PercentualUtilizacaoLimite": pd.Series(["0.92"], dtype="float64"), "QtdTransacoesNegadas": pd.Series(["5.0"], dtype="float64"), "AnosDeRelacionamentoBanco": pd.Series(["3.0"], dtype="float64"), "JaUsouChequeEspecial": pd.Series(["0.0"], dtype="float64"), "QtdEmprestimos": pd.Series(["1.0"], dtype="float64"), "NumeroAtendimentos": pd.Series(["7"], dtype="int64"), "TMA": pd.Series(["2"], dtype="int64"), "IndiceSatisfacao": pd.Series(["4"], dtype="int64"), "Saldo": pd.Series(["55229"], dtype="int64"), "CLTV": pd.Series(["65"], dtype="int64"), "CanalPref": pd.Series(["Push"], dtype="object")})
output_sample = np.array([0])
try:
    log_server.enable_telemetry(INSTRUMENTATION_KEY)
    log_server.set_verbosity('INFO')
    logger = logging.getLogger('azureml.automl.core.scoring_script')
except:
    pass


def init():
    global model
    # This name is model.id of model that we want to deploy deserialize the model file back
    # into a sklearn model
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'model.pkl')
    try:
        model = joblib.load(model_path)
    except Exception as e:
        path = os.path.normpath(model_path)
        path_split = path.split(os.sep)
        log_server.update_custom_dimensions({'model_name': path_split[1], 'model_version': path_split[2]})
        logging_utilities.log_traceback(e, logger)
        raise


@input_schema('data', PandasParameterType(input_sample))
@output_schema(NumpyParameterType(output_sample))
def run(data):
    try:
        result = model.predict(data)
        return json.dumps({"result": result.tolist()})
    except Exception as e:
        result = str(e)
        return json.dumps({"error": result})
