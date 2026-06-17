import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    nombre_tabla = os.environ["TABLE_NAME"]

    try:
        # Entrada (json)
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']

        # Proceso
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)

        # Log estandar INFO (ejecucion correcta)
        log = {
            "tipo": "INFO",
            "log_datos": pelicula
        }
        print(json.dumps(log))   # Log json estandar en CloudWatch

        # Salida (json)
        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }

    except Exception as e:
        # Log estandar ERROR (cuando algo falla)
        log = {
            "tipo": "ERROR",
            "log_datos": {
                "error": str(e),
                "evento": event.get('body', event)
            }
        }
        print(json.dumps(log))   # Log json estandar en CloudWatch

        # Salida (json) con el error controlado
        return {
            'statusCode': 500,
            'error': str(e)
        }
