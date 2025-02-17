# -*- coding: utf-8 -*-
"""Cópia de Hora da verdade (8) - tensorflow

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uk3Njgx8T5RRKP5fxXfdy0ywJdDj8NG3

#**PARTE 1 -** Base de dados

##**1.1 -** Leitura ESC-50 e Audioset

ESC-50
- Mais fácil, já está com o df praticamente pronto
"""

# Commented out IPython magic to ensure Python compatibility.
!git clone https://github.com/karolpiczak/ESC-50.git
# %cd ESC-50

import pandas as pd
metadados = pd.read_csv('meta/esc50.csv')
metadados.head()
#print(len(metadados))

#Dicionário
target_category_dict = dict(zip(metadados['target'], metadados['category']))
target_category_dict

list_to_keep = ['church_bells','siren','dog','crying_baby','fireworks','footsteps','clock_alarm','train','cat']
df_esc = metadados[metadados['category'].isin(list_to_keep)]
print(df_esc.head())
print(len(df_esc))

"""Audioset
- Vamos precisar criar um df com o filename e o label
"""

import pandas as pd

!pip install gdown
import gdown
import zipfile

#https://drive.google.com/file/d/1RAD1x5Y72Ntl91D4a0l0sPnrLm6T3mf7/view?usp=sharing

# Baixar o arquivo ZIP do Google Drive
file_id = "1RAD1x5Y72Ntl91D4a0l0sPnrLm6T3mf7"
url = f"https://drive.google.com/uc?id={file_id}"
output = "/content/audios_audioset.zip"
gdown.download(url, output, quiet=False)

# Extrair o arquivo ZIP
with zipfile.ZipFile(output, 'r') as zip_ref:
    zip_ref.extractall("/content/audios_audioset")

# Verificar arquivos extraídos
import os

extracted_path = "/content/audios_audioset"
print(os.listdir(extracted_path))

#código da lele

!pip install gdown
import gdown
import zipfile

#https://drive.google.com/file/d/1JcwGinPkjO6HmB2lW0ahuWpBZ2BmoV5f/view?usp=sharing


# Baixar o arquivo ZIP do Google Drive
file_id = "1JcwGinPkjO6HmB2lW0ahuWpBZ2BmoV5f"
url = f"https://drive.google.com/uc?id={file_id}"
output = "/content/audios_total.zip"
gdown.download(url, output, quiet=False)

# Extrair o arquivo ZIP
with zipfile.ZipFile(output, 'r') as zip_ref:
    zip_ref.extractall("/content/audios_total")

# Verificar arquivos extraídos
import os

extracted_path = "/content/audios_total"
print(os.listdir(extracted_path))

#Criar um df com o nome dos áudios e os labels
audio_files = os.listdir("/content/audios_total")

filename = []
label = []

for file in audio_files:
  filename.append(file)
  label.append(file[12:].split(".")[0])

df_audioset = pd.DataFrame({'filename': filename, 'label': label})
df_audioset.head()
#len(df_audioset)

df_audioset['label'].value_counts().to_string()

labels_to_keep = ['crying_baby','siren','doorbell']

df_audioset2 = df_audioset[df_audioset['label'].isin(labels_to_keep)]
df_audioset2.head()

df_audioset2['filename_prefix'] = df_audioset2['filename'].str[:12]
print("Número de duplicatas antes de remover:", df_audioset2['filename_prefix'].duplicated().sum())

df_audioset2.drop_duplicates(subset='filename_prefix', inplace=True)
print("Número de duplicatas após remoção:", df_audioset2['filename_prefix'].duplicated().sum())

df_audioset2.drop(columns=['filename_prefix'], inplace=True)
print("Verificação final de duplicatas:", df_audioset2['filename'].duplicated().sum())

print(df_audioset2)

df_audioset2['label'].value_counts()

'''#Subamostrar a quantidade de itens shotgun, de modo que diminua pra 50

shotgun_df = df_audioset2[df_audioset2['label'] == 'shotgun']
shotgun_df_sampled = shotgun_df.sample(n=50)
df_audioset2 = pd.concat([df_audioset2[df_audioset2['label'] != 'shotgun'], shotgun_df_sampled])

df_audioset2['label'].value_counts()

df_audioset2

"""##**1.2 -** Juntar os dois df
(Onde as filhas choram e as mães não veem)
"""

df_esc1 = df_esc.drop(columns=['target','esc10','src_file','take'])
df_esc1 = df_esc1.rename(columns={'category': 'label'})
df_esc1.head()

import numpy as np

# Criar uma nova coluna "fold" no df_audioset2
df_audioset2["fold"] = np.random.randint(1, 5, size=len(df_audioset2))

# Manter uma boa quantia de classes para divisão
df_audioset2["fold"] = df_audioset2["fold"].apply(lambda x: x if x != 5 else np.random.randint(1, 5))

# Exibir o df_audioset2 atualizado
print(df_audioset2)

df = pd.concat([df_esc1, df_audioset2], ignore_index=True)
print(df.head())
print(len(df))
print(df['label'].value_counts())

"""Concentrar os áudios em uma só pasta"""

import os
import shutil

filenames = df['filename'].tolist()

# Create the destination directory
destination_dir = "/content/audios_df"
os.makedirs(destination_dir, exist_ok=True)

audioset_dir = '/content/audios_audioset'
audioesc_dir = '/content/ESC-50/audio'

audioset = os.listdir(audioset_dir)
audioesc = os.listdir(audioesc_dir)

for filename in filenames:
    filename_with_ext = filename
    if filename_with_ext in audioset:
        source_path = os.path.join(audioset_dir, filename_with_ext)
        destination_path = os.path.join(destination_dir, filename_with_ext)
        try:
            shutil.copyfile(source_path, destination_path)
        except Exception as e:
            print(f"Failed to copy {filename_with_ext} from audioset: {e}")
    elif filename_with_ext in audioesc:
        source_path = os.path.join(audioesc_dir, filename_with_ext)
        destination_path = os.path.join(destination_dir, filename_with_ext)
        try:
            shutil.copyfile(source_path, destination_path)
        except Exception as e:
            print(f"Failed to copy {filename_with_ext} from audioesc: {e}")
    else:
        print(f"{filename_with_ext} not found in either audioset or audioesc")

# Verify the number of files that have been copied
copied_files = os.listdir(destination_dir)
print(f"Number of audio files copied: {len(copied_files)}")

"""#**PARTE 2 -** Pré-Processamento

##**2.1 -** Tratamento da base
"""

!pip install -q "tensorflow==2.11.*"
!pip install -q tensorflow-io

#Conferir se o tensorflow_io está mesmo instalado

import tensorflow_io as tfio
print(tfio.__version__)

import os

from IPython import display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_io as tfio

import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import csv

from IPython.display import Audio
from scipy.io import wavfile

"""Puxando o modelo"""

yamnet_model_handle = 'https://tfhub.dev/google/yamnet/1'
yamnet_model = hub.load(yamnet_model_handle)

"""Conferir as labels que o modelo oferece e adequar o nosso dicionário a elas"""

class_map_path = yamnet_model.class_map_path().numpy().decode('utf-8')
class_names =list(pd.read_csv(class_map_path)['display_name'])
fim = len(class_names)

for name in class_names[:fim]:
  print(name)
print('...')

#transformar as labels

def format_label(label):
    words = label.split('_')
    if len(words) > 1:
        formatted_label = words[0].capitalize() + ' ' + words[1].lower()
    else:
        formatted_label = words[0].capitalize()
    return formatted_label

df_esc1['label'] = df_esc1['label'].apply(format_label)
df_esc1.head()

label_map = {
    'Shotgun': 'Gunfire',
    'Door wood knock':'Knock',
    'Chirping birds': 'Birds',
    'Laughing': 'Laughter',
    'Crying baby': 'Infant cry',
    'Insects': 'Insect',
    'Crackling fire': 'Fire',
    'Sea waves': 'Waves',
    'Door wood': 'Door'
}

# Substituindo
df_esc1['label'] = df_esc1['label'].replace(label_map)

print(len(df_esc1['label'].unique()))
print(df_esc1['label'].unique())
my_classes = df_esc1['label'].unique()
print(my_classes)

"""Copiar o caminho do áudio em filename"""

base_data_path = '/content/ESC-50/audio'
full_path = df_esc1['filename'].apply(lambda row: os.path.join(base_data_path, row))
df_nomeado = df_esc1.assign(filename=full_path)

df_nomeado.head(10)

"""##**2.2 -** Tratamento dos dados e criação da base

Criando um df com tensor flow
"""

from sklearn.preprocessing import LabelEncoder

#Mapeamento das labels
label_encoder = LabelEncoder()
df_nomeado['label_encoded'] = label_encoder.fit_transform(df_nomeado['label'])
df_nomeado.head(5)

filenames = df_nomeado['filename']
targets = df_nomeado['label_encoded']
folds = df_nomeado['fold']

df_yamnet = tf.data.Dataset.from_tensor_slices((filenames, targets, folds))
df_yamnet.element_spec
#print(df_yamnet)

"""É preciso se certificar que os audios tenham uma taxa de amostragem de 16kHz e tenha só um canal de áudio (MONO)"""

import tensorflow as tf
import scipy.signal

# Função para reamostrar o áudio
def ensure_sample_rate(original_sample_rate, waveform, desired_sample_rate=16000):
    """Reamostrar waveform se necessário."""
    if original_sample_rate != desired_sample_rate:
        desired_length = int(round(float(len(waveform)) / original_sample_rate * desired_sample_rate))
        waveform = scipy.signal.resample(waveform, desired_length)
    return desired_sample_rate, waveform

# Função de carregamento de áudio e reamostragem
def load_wav_for_map(filename, label, fold):
    file_contents = tf.io.read_file(filename)
    wav, original_sample_rate = tf.audio.decode_wav(
        file_contents,
        desired_channels=1)
    wav = tf.squeeze(wav, axis=-1)
    original_sample_rate = int(original_sample_rate.numpy())
    _, wav = ensure_sample_rate(original_sample_rate, wav.numpy())
    return wav, label, fold

# Função para usar tf.py_function e evitar problemas de forma
def load_wav_for_map_tf(filename, label, fold):
    audio, label, fold = tf.py_function(load_wav_for_map, [filename, label, fold], [tf.float32, tf.int64, tf.int64])
    audio.set_shape([None])  # Definir forma variável para o áudio
    label.set_shape([])
    fold.set_shape([])
    return audio, label, fold

# Mapear a função de carregamento e reamostragem
df_yamnet = df_yamnet.map(load_wav_for_map_tf, num_parallel_calls=tf.data.AUTOTUNE)
df_yamnet.element_spec

"""##**2.3 -** Extração das features"""

# applies the embedding extraction model to a wav data
def extract_embedding(wav_data, label, fold):

  # Normalização para o intervalo [-1.0, 1.0]
  #wav_data_normalized = tf.cast(wav_data, tf.float32) / tf.int16.max

  #run YAMNet to extract embedding from the wav data
  scores, embeddings, spectrogram = yamnet_model(wav_data)
  num_embeddings = tf.shape(embeddings)[0]
  return (embeddings,
            tf.repeat(label, num_embeddings),
            tf.repeat(fold, num_embeddings))

# extract embedding
df_yamnet = df_yamnet.map(extract_embedding).unbatch()
df_yamnet.element_spec

"""##**2.4 -** Dividir os dados

A gente vai usar a coluna de fold para dividir o conjunto de dados em conjuntos de treinamento, validação e teste.

O ESC-50 está organizado em cinco fold de validação cruzada de tamanho uniforme, de modo que os clipes da mesma fonte original estejam sempre na mesma fold - saiba mais no documento ESC: Dataset for Environmental Sound Classification .

A última etapa é remover a coluna de fold do conjunto de dados, pois você não a usará durante o treinamento.
"""

cached_ds = df_yamnet.cache()
train_ds = cached_ds.filter(lambda embedding, label, fold: fold < 4)
val_ds = cached_ds.filter(lambda embedding, label, fold: fold == 4)
test_ds = cached_ds.filter(lambda embedding, label, fold: fold == 5)

#Remover as colunas 'fold' que não precisamos mais
remove_fold_column = lambda embedding, label, fold: (embedding, label)

train_ds = train_ds.map(remove_fold_column)
val_ds = val_ds.map(remove_fold_column)
test_ds = test_ds.map(remove_fold_column)

#Pré processamento adicional
#Armazena em cache, garante a variação dos dados, agrupa os dados em lotes
      #para atualização mais rápida e permite um melhor gerenciamento de recursos

train_ds = train_ds.cache().shuffle(1000).batch(32).prefetch(tf.data.AUTOTUNE)
val_ds = val_ds.cache().batch(32).prefetch(tf.data.AUTOTUNE)
test_ds = test_ds.cache().batch(32).prefetch(tf.data.AUTOTUNE)

"""#**PARTE 3 -** Modelo"""

my_model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(1024), dtype=tf.float32,
                          name='input_embedding'),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(len(my_classes))
], name='my_model')

my_model.summary()

my_model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                 optimizer="adam",
                 metrics=['accuracy'])

callback = tf.keras.callbacks.EarlyStopping(monitor='loss',
                                            patience=3,
                                            restore_best_weights=True)

history = my_model.fit(train_ds,
                       epochs=20,
                       validation_data=val_ds,
                       callbacks=callback)

loss, accuracy = my_model.evaluate(test_ds)

print("Loss: ", loss)
print("Accuracy: ", accuracy)

"""3.1 Testando com yamnet

"""

testing_wav_file_name = tf.keras.utils.get_file('doorbell.wav',
                                                'https://storage.googleapis.com/audioset/yamalyzer/audio/doorbell.wav',
                                                cache_dir='./',
                                                cache_subdir='test_data')

print(testing_wav_file_name)

import tensorflow as tf
import scipy.signal
import matplotlib.pyplot as plt
import IPython.display as display

# Função para reamostrar o áudio
def ensure_sample_rate(original_sample_rate, waveform, desired_sample_rate=16000):
    """Reamostrar waveform se necessário."""
    if original_sample_rate != desired_sample_rate:
        desired_length = int(round(float(len(waveform)) / original_sample_rate * desired_sample_rate))
        waveform = scipy.signal.resample(waveform, desired_length)
    return desired_sample_rate, waveform

# Função de carregamento de áudio e reamostragem
def load_wav_for_map(filename, label):
    file_contents = tf.io.read_file(filename)
    wav, original_sample_rate = tf.audio.decode_wav(
        file_contents,
        desired_channels=1)
    wav = tf.squeeze(wav, axis=-1)
    original_sample_rate = int(original_sample_rate.numpy())
    _, wav = ensure_sample_rate(original_sample_rate, wav.numpy())
    return wav, label

# Função para usar tf.py_function e evitar problemas de forma
def load_wav_for_map_tf(filename, label):
    audio, label = tf.py_function(load_wav_for_map, [filename, label], [tf.float32, tf.int64])
    audio.set_shape([None])  # Definir forma variável para o áudio
    label.set_shape([])
    return audio, label

testing_wav_data, testing_label = load_wav_for_map_tf(testing_wav_file_name, tf.constant(0, dtype=tf.int64))

# Plotar o áudio
_ = plt.plot(testing_wav_data.numpy())
plt.show()

# Tocar o arquivo de áudio
display.display(display.Audio(testing_wav_data.numpy(), rate=16000))

class_map_path = yamnet_model.class_map_path().numpy().decode('utf-8')
class_names_yamnet =list(pd.read_csv(class_map_path)['display_name'])

for name in class_names_yamnet[:20]:
  print(name)
print('...')

scores, embeddings, spectrogram = yamnet_model(testing_wav_data)
class_scores = tf.reduce_mean(scores, axis=0)
top_class = tf.math.argmax(class_scores)
inferred_class = class_names_yamnet[top_class]

print(f'The main sound is: {inferred_class}')
print(f'The embeddings shape: {embeddings.shape}')

import tensorflow as tf

# Defina o caminho onde o modelo será salvo no ambiente do Colab
model_path = '/content/saved_model/'

# Salvar o modelo como SavedModel
model = yamnet_model
tf.saved_model.save(model, model_path)

# Converter para TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_saved_model(model_path)
tflite_model = converter.convert()

# Salvar o modelo TensorFlow Lite em um arquivo .tflite
tflite_model_path = '/content/model.tflite'
with open(tflite_model_path, 'wb') as f:
    f.write(tflite_model)

print(f'Modelo TensorFlow Lite salvo em {tflite_model_path}')

