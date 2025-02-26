import os
import requests
import base64
import pandas as pd

# Função para fazer o upload das imagens para o ImgBB
def upload_to_imgbb(folder_path, api_key):
    uploaded_images = []

    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):  # Verifique se é uma imagem
            file_path = os.path.join(folder_path, filename)

            # Abra a imagem e converta para base64
            with open(file_path, 'rb') as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')

            # Dados para o upload
            data = {
                'key': api_key,
                'image': image_data,
                'name': filename  # Nome original da imagem
            }

            # Realiza o upload
            response = requests.post('https://api.imgbb.com/1/upload', data=data)

            # Verifica se o upload foi bem-sucedido
            if response.status_code == 200:
                json_response = response.json()
                uploaded_images.append({
                    'name': filename,
                    'link': json_response['data']['url']  # Link da imagem
                })
                print(f"Upload da imagem {filename} realizado com sucesso. Link: {json_response['data']['url']}")
            else:
                print(f"Erro ao fazer upload da imagem {filename}: {response.text}")

    return uploaded_images

# Função para salvar os nomes e links das imagens em um arquivo Excel
def save_to_excel(data, excel_path):
    df = pd.DataFrame(data)
    df.to_excel(excel_path, index=False)

# Configurações
folder_path = r'Caminho_para_pasta'  # Caminho para a pasta
api_key = 'Chave_API'  # Insira sua chave da API do ImgBB
excel_path = r'caminho_arquivo\arquivo.xlsx'  # Caminho para o arquivo Excel

# Executa o upload e obtém os links e nomes
links_nomes_imagens = upload_to_imgbb(folder_path, api_key)

# Salva os links e nomes das imagens em um arquivo Excel
save_to_excel(links_nomes_imagens, excel_path)

# Exibe os links e nomes das imagens
print("\nImagens carregadas:")
for item in links_nomes_imagens:
    print(f"Nome: {item['name']}, Link: {item['link']}")
