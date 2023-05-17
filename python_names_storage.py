from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
    "type": "service_account",
  "project_id": "moonlit-buckeye-382223",
  "private_key_id": "ec4c93de9def626057da16422ad2c541929949d1",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCVUWXoPQIj0s1o\n0n3OGfVSrtEP45tNIeHJMPpUxTdpYas/cDuqiupoba/iX7vzxPD7zpATpv7mEKVs\n+uOMn8zGEjjwgg3uWvBkM4gGRVczhtTiPToyFGHJ5Adlq+0kJkqq0eEj+i48PDEm\nBSZcHFRikYCHDWnUJyxS2e9c5gKkyTEduPD/rSJvyBkAH3FczT5kkPoyqNWynQZX\nbb4Q4dw0Y4cNZclGFrWGIFFUED9Vr3ebfG7znGjhpPIE9IhPUyaWVUhQ+37mJPPH\nF60MDhL+xU9YRdr8Bfm4yJ9CDiYqR4InxuZvq5OG2VnI9XZnWTfTmRpWxSRIe5HR\nQgluZmjnAgMBAAECggEAK9Uhw7uJEcgTmYZU/PgczoFYCMCJeeqM09lHWzQrsIlF\n0pEZStaNukscuyjcTVKOZXT9UW+P2yyeyy+ZNdJBNBHsWhnrigFzGQ8Rirm3P/6A\nJsvPdh0KmdARJdUC/74n5B5JZ5zNDsyipuUTHi4IzYimAL88xlUbi1TDkfNJamLc\nWsuSzdph97xZ5ODv3jBjhyVqxKiYX4a10QPRznsAuBv13ep5FSFD3VP5cmzWiCOa\nZESorQ8NqP+KtxwSSC1gBVfaKIOHiR8lUbXgxuQb+yX8WG0UjmAs2yJ6UhtcIw6s\nDEjx5eOLnM3lkP5FQDxCyGke+/BJ1CcReavds6LToQKBgQDMktsuMB4zm12vNccI\nV0KKkzVG1uPo7mqf5I9rFH10o7zwsHepZFDhnyB6nleInHNci9P/ETB0+7Vfqd7M\nOKr+7hL7DYjOzGpZoFEriJvxuoEJNFU6kZD/6fDX+ALVQE8ndB3pLIO5yznjhY1J\nenEy1D4jXes2BEDdy3PZBTM9RwKBgQC62p0tAxsWbcOQ6mIkCc2crVTIRNSUaJso\nrR3TbKLnOkFB7WOphkjwMOgaRpSiI3QNmLc9zwLJj/jgeiU9CIXqDRyeCxQagwPv\nlrcJf0hIQHEEhsatehbUA1HjNk0ndUsWRd317QkooUn2OLXnLbPxlmMYtCHSsHQj\nwWQyWNbHYQKBgGboDNdsHxUot3S2oZtBgdiBepBa8qSuofYynC5qTT2KTDXrHxaX\nvtPwHv9vfWrcAG/yar7pH64JHFC1+7xRWTsJ+YROZ55XV7wkGBDFFGUBw30k1Sa0\nKPOC88NAH/Sz991J3O35lX21jDY2bT8kF6NQ/rz9tp8ifprTiEAIDKFrAoGBALob\nYi9iB4nIW+ArwwI4DWX/MhGilMUYh2n1O17ItlxuJm8+vWQtDtrFK3h4UjRH8aBV\nOjXCyPjvgCg9IHfw1EixNI6pZCWf1ry8taQs9VaZcLfccWh50ODsSZRwElq5tccC\nYbg/lj60ntEx3OPcHn0Cl8MULxgFjjfKuDx5RbshAoGBAMHaGAcezsi10bzddyI/\n4jCa05vQQjRE2wnLSP4t59hzCgWaOeFlCKQ0diWdh45Jbikfx/yx5wgC4u/DEaGX\n8buTyiHMetq9pXFCdMsh1ci0D3TAbDKGJ8NdVK+75/k/iyuLrbpPGDde2tnqSKgZ\nzxuyAtJXg8ntFdClgSPBxMG2\n-----END PRIVATE KEY-----\n",
  "client_email": "pmcardamone@moonlit-buckeye-382223.iam.gserviceaccount.com",
  "client_id": "116227407277652709047",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/pmcardamone%40moonlit-buckeye-382223.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"  
}

try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('bucket_dataops1605') ### Nome do seu bucket
  blob = bucket.blob('artist-names.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 
