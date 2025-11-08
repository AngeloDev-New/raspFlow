from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/drive']

class Folder:
    def __init__(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json', SCOPES)
        self.creds = flow.run_local_server(port=0)
        self.service = build('drive', 'v3', credentials=self.creds)

        self.current_folder_id = 'root'
        self.path_stack = ['root']  # histórico de pastas

    def pwd(self):
        print("Caminho atual:", " / ".join(self.path_stack))
        return self.current_folder_id

    def ls(self):
        results = self.service.files().list(
            q=f"'{self.current_folder_id}' in parents and trashed=false",
            pageSize=100,
            fields="files(id, name, mimeType, shortcutDetails)").execute()
        items = results.get('files', [])

        print(f"{'Tipo':<10} {'Nome':<50} {'ID':<35} {'Link'}")
        print("-"*130)
        for item in items:
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                tipo = 'DIR'
                link = f"https://drive.google.com/drive/folders/{item['id']}"
            elif item['mimeType'] == 'application/vnd.google-apps.shortcut':
                tipo = 'SHORTCUT'
                # pega o ID do destino do shortcut
                link = f"https://drive.google.com/drive/folders/{item['shortcutDetails']['targetId']}"
            else:
                tipo = 'FILE'
                link = f"https://drive.google.com/file/d/{item['id']}/view"

            print(f"{tipo:<10} {item['name']:<50} {item['id']:<35} {link}")
        return items

    def cd(self, folder_name):
        if folder_name == "..":
            if len(self.path_stack) > 1:
                self.path_stack.pop()
                self.current_folder_id = self.path_stack[-1]
                print("Voltando para pasta anterior")
            else:
                print("Já está na raiz")
            return

        results = self.service.files().list(
            q=f"'{self.current_folder_id}' in parents and name='{folder_name}' and trashed=false",
            fields="files(id, name, mimeType, shortcutDetails)").execute()
        items = results.get('files', [])
        if not items:
            print("Pasta não encontrada")
            return

        target = items[0]
        if target['mimeType'] == 'application/vnd.google-apps.folder':
            self.current_folder_id = target['id']
            self.path_stack.append(target['id'])
            print(f"Agora em: {folder_name}")
        elif target['mimeType'] == 'application/vnd.google-apps.shortcut':
            # entra na pasta destino do shortcut
            dest_id = target['shortcutDetails']['targetId']
            self.current_folder_id = dest_id
            self.path_stack.append(dest_id)
            print(f"Agora em (shortcut): {folder_name}")
        else:
            print(f"{folder_name} não é uma pasta nem shortcut navegável")

    def get(self, file_name, dest_path):
        # Baixa um arquivo pelo nome
        results = self.service.files().list(
            q=f"'{self.current_folder_id}' in parents and name='{file_name}' and trashed=false",
            fields="files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print("Arquivo não encontrado")
            return
        file_id = items[0]['id']

        request = self.service.files().get_media(fileId=file_id)
        with open(dest_path, 'wb') as f:
            from googleapiclient.http import MediaIoBaseDownload
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%")
        print("Download concluído!")

    def set(self, file_path, drive_name=None):
        # Faz upload de um arquivo para a pasta atual
        from googleapiclient.http import MediaFileUpload
        if not drive_name:
            drive_name = os.path.basename(file_path)
        file_metadata = {
            'name': drive_name,
            'parents': [self.current_folder_id]
        }
        media = MediaFileUpload(file_path, resumable=True)
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"Arquivo enviado: {file.get('id')}")
