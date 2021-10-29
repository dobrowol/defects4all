import tensorflow as tf
import numpy as np

import tensorflow as tf
import matplotlib.pyplot as plt
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder

def plot_graphs(history, metric):
  plt.plot(history.history[metric])
  plt.plot(history.history['val_'+metric], '')
  plt.xlabel("Epochs")
  plt.ylabel(metric)
  plt.legend([metric, 'val_'+metric])


DATASET_SIZE=863
BATCH_SIZE =64
train_size = int(0.75 * DATASET_SIZE)
test_size = int(0.25 * DATASET_SIZE)

file_with_klogs = "klogs_raw.tsv"
file_with_labels = "labels.vec"
with open(file_with_klogs) as f:
    lines = f.readlines()
    DATASET_SIZE = len(lines)
    max_sentence_len = 0
    for line in lines:
        splitted_len = len(line.split())
        if splitted_len > max_sentence_len:
            max_sentence_len = splitted_len
    print("Data size ", DATASET_SIZE)
with open(file_with_labels) as label_file:
    label_lines = label_file.readlines()
    encoder = LabelEncoder()
    encoder.fit(label_lines)
    encoded_Y = encoder.transform(label_lines)
    # convert integers to dummy variables (i.e. one hot encoded)
    dummy_y = np_utils.to_categorical(encoded_Y)
    print(dummy_y[:1])
klogs_ds = tf.data.TextLineDataset(file_with_klogs)
labels_ds = tf.data.Dataset.from_tensor_slices(dummy_y)
klogs_labels_ds = tf.data.Dataset.zip((klogs_ds, labels_ds))
klogs_labels_ds = klogs_labels_ds.shuffle(DATASET_SIZE, reshuffle_each_iteration=True)
train_dataset = klogs_labels_ds.take(train_size)
test_dataset = klogs_labels_ds.skip(train_size)
test_dataset = klogs_labels_ds.take(test_size)

print(f"{train_dataset.element_spec}")

print(list(train_dataset.take(1).as_numpy_iterator()))

print(f"{test_dataset.element_spec}")

for example, label in test_dataset.take(1):
  print('text: ', example.numpy())
  print('label: ', label.numpy())

train_dataset = train_dataset.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
test_dataset = test_dataset.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
klogs_labels_ds = klogs_labels_ds.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
klogs_labels_ds.repeat()

VOCAB_SIZE = 4096
encoder = tf.keras.layers.TextVectorization(
    max_tokens=VOCAB_SIZE,
    output_sequence_length=max_sentence_len)
encoder.adapt(klogs_labels_ds.map(lambda text, label: text))
encoded_example = encoder(example).numpy()
print(encoded_example)
vocab = np.array(encoder.get_vocabulary())
print(vocab[:20])

model = tf.keras.Sequential([
    encoder,
    tf.keras.layers.Embedding(
        input_dim=len(encoder.get_vocabulary()),
        output_dim=BATCH_SIZE,
        # Use masking to handle the variable sequence lengths
        mask_zero=True),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(BATCH_SIZE)),
    tf.keras.layers.Dense(BATCH_SIZE, activation='relu'),
    tf.keras.layers.Dense(DATASET_SIZE, activation='softmax')
])
print([layer.supports_masking for layer in model.layers])
model.compile(loss='categorical_crossentropy',
              optimizer=tf.keras.optimizers.Adam(1e-4),
              metrics=['accuracy'])
print (model.summary())
steps_per_epoch = DATASET_SIZE//BATCH_SIZE
print(steps_per_epoch)
history = model.fit(klogs_labels_ds, epochs=10,
 #                   steps_per_epoch=steps_per_epoch,
                    validation_data=klogs_labels_ds,
                    validation_steps=10)


