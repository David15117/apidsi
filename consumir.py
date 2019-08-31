import io
import os
from google.cloud import vision
from google.cloud.vision import types
from google.cloud import translate
translate_client = translate.Client()
import argparse

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'token2.json'
client = vision.ImageAnnotatorClient()
translate_client = translate.Client()

target = 'pt-br'

print(client)
print(translate_client)



file_name = os.path.join(os.path.dirname(__file__),'img/rosto.png')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
  content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)


#detecta mensagem atraves da imagem
def detec_faces_uri(uri):

  image = vision.types.Image()
  image.source.image_uri = uri
  #resposta da API
  response = client.face_detection(image=image)
  faces = response.face_annotations
  #tratamento possibilidades: Melhor dzeindo estados
  likelihood_name = ('DESCONHECIDO', 'MUITO IMPROVÁVEL', 'IMPROVÁVEL', 'POSSÍVEL','PROVÁVEL', 'MUITO PROVÁVEL')
  print('Faces:')

  for face in faces:
    print('Raiva: {}'.format(likelihood_name[face.anger_likelihood]))
    print('Alegria: {}'.format(likelihood_name[face.joy_likelihood]))
    print('Surpresa: {}'.format(likelihood_name[face.surprise_likelihood]))
    #para imprimir a API
    print(face)
    print('Tristeza: {}'.format(likelihood_name[face.sorrow_likelihood]))
    # ângulo do rolo: -22,071542739868164
    # ângulo de panela: -7.378933429718018
    # ângulo de inclinação: -25.574338912963867
    # detecção de confiança: 0.549518346786499
    # confiança de landmarking: 0.4459625482559204
    # probabilidade de alegria: MUITO PROVÁVEL
    # verossimilhança: MUITO INJUSTAMENTE
    # probabilidade de raiva: MUITO INCRIVEL
    # probabilidade de surpresa: MUITO INJUSTA
    # under exposed_likelihood: MUITO INJUSTA
    # probabilidade borrada: MUITO INJUSTA
    # probabilidade de headwear: MUITO INJUSTAMENTE
#rotulos da api caracteristicas etc. por exemplo cachorro etc.
def detecta_labels_uri(uri):

  image = vision.types.Image()
  image.source.image_uri = uri

  response = client.label_detection(image=image)
  labels = response.label_annotations

  for label in labels:
    #retorna o label ou seja a descrição descrita na API
    text = label.description
    translation = translate_client.translate(text, target_language=target)
    print(translation['translatedText'])
#detecta pontos de referencias
#Botafogo Beach
#Sugarloaf Mountain
#Estádio do Maracanã
#Lagoa
def detecta_referencia_uri(uri):

    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations

    print('Landmarks:')
    for text in landmarks:
        texto = text
        translation = translate_client.translate(str(texto), target_language=target)
        print(translation['translatedText'])

#detecta logo das imagens o exemplo a seguir apresenta nick
def detecta_logos_uri(uri):

  image = vision.types.Image()
  image.source.image_uri = uri

  response = client.logo_detection(image=image)
  logos = response.logo_annotations
  print('Logos:')
  for logo in logos:
    print(logo.description)
    #text = logo.description
    #translation = translate_client.translate(text, target_language=target)
    #print(translation['translatedText'])

#imprime texto nas imagens
def detecta_texto_uri(uri):
  final = " "
  image = vision.types.Image()
  image.source.image_uri = uri

  response = client.text_detection(image=image)
  texts = response.text_annotations
  print('Texts:')
  for text in texts:
      final= final+' '+text.description
  print(final)

def  detecta_crop_hints(uri):
    image = vision.types.Image()
    image.source.image_uri = uri

    crop_hints_params = vision.types.CropHintsParams(aspect_ratios=[1.77])
    image_context = vision.types.ImageContext(crop_hints_params=crop_hints_params)

    response = client.crop_hints(image=image, image_context=image_context)
    hints = response.crop_hints_annotation.crop_hints

    for n, hint in enumerate(hints):
        print('\nCrop Hint: {}'.format(n))
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                     for vertex in hint.bounding_poly.vertices])
        print('bounds: {}'.format(','.join(vertices)))

#localizar Objetos no ambiente
def localizar_objects_uri(uri):
    image = vision.types.Image()
    image.source.image_uri = uri

    objects = client.object_localization(image=image).localized_object_annotations
    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        text = object_.name
        translation = translate_client.translate(text, target_language=target)
        print(translation['translatedText'])


def web_entities_include_geo_results_uri(uri):

    image = vision.types.Image()
    image.source.image_uri = uri

    web_detection_params = vision.types.WebDetectionParams(include_geo_results=True)
    image_context = vision.types.ImageContext(web_detection_params=web_detection_params)

    response = client.web_detection(image=image, image_context=image_context)

    for entity in response.web_detection.web_entities:

        text = entity.description
        translation = translate_client.translate(text, target_language=target)
        print(translation['translatedText'])

def detect_web_annotations_uri(uri):
    image = vision.types.Image()
    image.source.image_uri = uri

    web_detection_params = vision.types.WebDetectionParams(include_geo_results=True)
    image_context = vision.types.ImageContext(web_detection_params=web_detection_params)

    response = client.web_detection(image=image, image_context=image_context)


    for entity in response.web_detection.web_entities:
        text=entity.description

        translation = translate_client.translate(text, target_language=target)
        print(translation['translatedText'])


####

#detecta_labels_uri("http://data.biovet.com.br/file/2018/10/29/H104520-F00000-V006-2000x0.jpeg")
#detecta_texto_uri("https://www.frasesdobem.com.br/wp-content/uploads/2018/07/que-a-alegria.jpg")
#detec_faces_uri("http://moyaortodontia.com.br/wp-content/uploads/2016/01/sorria-....jpg")

####

#detecta_referencia_uri("http://crddrj.com.br/wp-content/uploads/2018/07/02.jpg")
#detecta_logos_uri("https://i.pinimg.com/originals/29/dc/ee/29dceecd7f13a9869c30a8d3b8a86064.jpg")
#detecta_crop_hints("https://correiodaamazonia.com/wp-content/uploads/2018/01/indios.jpg")
#localizar_objects_uri("http://www.forumdaconstrucao.com.br/materias/imagens/02127_02.jpg")
#web_entities_include_geo_results_uri("http://www.folhadotocantins.com.br/wp-content/uploads/2019/04/07-34.jpg")
#detect_web_annotations_uri("https://image.flaticon.com/sprites/new_packs/125027-musical-symbols-and-annotations.png")