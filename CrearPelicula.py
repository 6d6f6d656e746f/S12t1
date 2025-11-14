import boto3
import uuid
import os
import json

def log_standard(tipo, log_datos):
    """Imprime logs en formato JSON estandarizado"""
    log_output = {
        "tipo": tipo,
        "log_datos": log_datos
    }
    print(json.dumps(log_output))

def lambda_handler(event, context):
    try:
        # Entrada (json)
        log_standard("INFO", {"mensaje": "Iniciando creación de película", "event": event})
        
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]
        
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
        
        # Salida (json)
        log_standard("INFO", {"mensaje": "Película creada exitosamente", "pelicula": pelicula, "response": response})
        
        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }
    
    except KeyError as e:
        log_standard("ERROR", {"mensaje": "Falta un parámetro requerido", "error": str(e)})
        return {
            'statusCode': 400,
            'error': f"Parámetro faltante: {str(e)}"
        }
    
    except Exception as e:
        log_standard("ERROR", {"mensaje": "Error procesando la solicitud", "error": str(e), "tipo_error": type(e).__name__})
        return {
            'statusCode': 500,
            'error': "Error interno del servidor"
        }
