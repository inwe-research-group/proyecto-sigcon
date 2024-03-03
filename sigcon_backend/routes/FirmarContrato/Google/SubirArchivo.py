from googleapiclient.http import MediaFileUpload
from routes.FirmarContrato.Google.Google import Create_Service
from routes.FirmarContrato.Google.ObtenerTokens import obtener_token



def subir_archivo(nom_archivo,ruta_archivo,tipos,nom_pariente):
    
    CLIENT_SECRET_FILE = "routes/FirmarContrato/Google/client_secret.json"
    API_NAME = "drive"
    API_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/drive"]

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    
    tipo_carpeta = ["application/vnd.google-apps.folder","application/vnd.google-apps.folder"]
    
    token_pariente,nom_pariente_aux =  obtener_token(nom_pariente,tipo_carpeta)

    file_metadata = {
        'name': nom_archivo,
        'parents': [token_pariente]
    }
    
    media_content = MediaFileUpload(ruta_archivo, mimetype='image/png')

    file = service.files().create(
        body=file_metadata,

        media_body=media_content
    ).execute()
    
    print(file)



def reemplazar_archivo(nom_archivo,ruta_archivo,tipos):
    CLIENT_SECRET_FILE = "Google/client_secret.json"
    API_NAME = "drive"
    API_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/drive"]

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    
    token_archivo, nom_archivo_aux = obtener_token(nom_archivo,tipos)

    media_content = MediaFileUpload(ruta_archivo, mimetype='image/png')

    file = service.files().update(
        fileId=token_archivo,
        media_body=media_content
    ).execute()
    
    print(file)