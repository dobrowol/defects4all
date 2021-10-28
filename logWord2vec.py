#@title Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import re
import string
import tqdm

import numpy as np

import tensorflow as tf
from tensorflow.keras import layers
import kmers
import argparse

from Log2Vec import Log2Vec

parser = argparse.ArgumentParser()

SEED=42
#sentence = "3 5 11 12 9 4 5 9 13 8"
#kms = kmers.createKmers(sentence, 3)


def generate_training_data(sequences, window_size, num_ns, vocab_size, seed):
    # Elements of each training example are appended to these lists.
    targets, contexts, labels = [], [], []

    # Build the sampling table for vocab_size tokens.
    sampling_table = tf.keras.preprocessing.sequence.make_sampling_table(vocab_size)

    # Iterate over all sequences (sentences) in dataset.
    for sequence in tqdm.tqdm(sequences):
        # Generate positive skip-gram pairs for a sequence (sentence).
        positive_skip_grams, _ = tf.keras.preprocessing.sequence.skipgrams(
          sequence,
          vocabulary_size=vocab_size,
          sampling_table=sampling_table,
          window_size=window_size,
          negative_samples=0)

        # Iterate over each positive skip-gram pair to produce training examples
        # with positive context word and negative samples.
        for target_word, context_word in positive_skip_grams:
            context_class = tf.expand_dims(
              tf.constant([context_word], dtype="int64"), 1)
            negative_sampling_candidates, _, _ = tf.random.log_uniform_candidate_sampler(
              true_classes=context_class,
              num_true=1,
              num_sampled=num_ns,
              unique=True,
              range_max=vocab_size,
              seed=seed,
              name="negative_sampling")

            # Build context and label vectors (for one target word)
            negative_sampling_candidates = tf.expand_dims(
              negative_sampling_candidates, 1)

            context = tf.concat([context_class, negative_sampling_candidates], 0)
            label = tf.constant([1] + [0]*num_ns, dtype="int64")

            # Append each element from the training example to global lists.
            targets.append(target_word)
            contexts.append(context)
            labels.append(label)

    return targets, contexts, labels

ut_log = "sentences.vec"
labels = "labels.vec"
with open(ut_log) as f:
  kms, kmers_vocab, kmers_in_line = kmers.createKmers(f.read().splitlines(), 3)
for line in kms[:20]:
  print(line)
#out_kl = io.open('klogs.tsv', 'w', encoding='utf-8')
#with open(labels) as f:
#    lines = f.read().splitlines()
#i=0
#for klog in kms:
#    out_kl.write(lines[i] + " " + klog + "\n")
#    i+=1
#out_kl.close()
kmers_ds = tf.data.Dataset.from_tensor_slices(kms)
vocab_size = 4096
sequence_length = 10

# Use the TextVectorization layer to normalize, split, and map strings to
# integers. Set output_sequence_length length to pad all samples to same length.
vectorize_layer = layers.TextVectorization(
    standardize=None,
    max_tokens=vocab_size,
    output_mode='int',
    output_sequence_length=sequence_length)
vectorize_layer.adapt(kmers_ds.batch(1024))
inverse_vocab = vectorize_layer.get_vocabulary()
print(inverse_vocab[:20])
AUTOTUNE = tf.data.AUTOTUNE
kmers_vector_ds = kmers_ds.batch(1024).prefetch(AUTOTUNE).map(vectorize_layer).unbatch()
sequences = list(kmers_vector_ds.as_numpy_iterator())
print(len(sequences))
for seq in sequences[:5]:
  print(f"{seq} => {[inverse_vocab[i] for i in seq]}")
num_ns = 4
targets, contexts, labels = generate_training_data(
    sequences=sequences,
    window_size=2,
    num_ns=num_ns,
    vocab_size=vocab_size,
    seed=SEED)

targets = np.array(targets)
contexts = np.array(contexts)[:,:,0]
labels = np.array(labels)

print('\n')
print(f"targets.shape: {targets.shape}")
print(f"contexts.shape: {contexts.shape}")
print(f"labels.shape: {labels.shape}")

BATCH_SIZE = targets.shape[0]
BUFFER_SIZE = 10000
dataset = tf.data.Dataset.from_tensor_slices(((targets, contexts), labels))
dataset = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)
print(dataset)
dataset = dataset.cache().prefetch(buffer_size=AUTOTUNE)
print(dataset)

embedding_dim = 128
word2vec = Log2Vec(vocab_size, embedding_dim, num_ns)
word2vec.compile(optimizer='adam',
                 loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
                 metrics=['accuracy'])
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir="logs")
word2vec.fit(dataset, epochs=20, callbacks=[tensorboard_callback])

weights = word2vec.get_layer('w2v_embedding').get_weights()[0]
vocab = vectorize_layer.get_vocabulary()

out_v = io.open('vectors.tsv', 'w', encoding='utf-8')
out_m = io.open('metadata.tsv', 'w', encoding='utf-8')

word2vecind={}
for index, word in enumerate(vocab):
  if index == 0:
    continue  # skip 0, it's padding.
  vec = weights[index]
  word2vecind[word] = index
  out_v.write('\t'.join([str(x) for x in vec]) + "\n")
  out_m.write(word + "\n")
out_v.close()
out_m.close()

import math

sequences_vectors = []
index = 0
for seq in sequences:

    word_vector = np.zeros(embedding_dim)
    for i in seq:
        if i == 0:
            break
        tf = math.log(kmers_vocab[inverse_vocab[i]]/len(sequences))  #term frequency
        idf = kmers_in_line[index][inverse_vocab[i]]/len(seq)  #inverse document frequency
        word_vector += tf*idf*weights[word2vecind[inverse_vocab[i]]]
    sequences_vectors.append(word_vector)
    index += 1

out_sv = io.open('sentences_vectors.tsv', 'w', encoding='utf-8')
for sent_vec in sequences_vectors:
    out_sv.write('\t'.join([str(x) for x in sent_vec]) + "\n")
out_sv.close()

print("sentence vectors len ", len(sequences_vectors))
with open("labels.vec") as label_file:
    labels_count = len(label_file.readlines())
print("num of labels", labels_count)