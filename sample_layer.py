from keras import backend as K
from keras.engine.topology import Layer
import numpy as np

np.set_printoptions(linewidth=9999)

# class Sample(Layer):
#     def __init__(self, output_dim, **kwargs):
#         self.output_dim = output_dim
#         super(Sample, self).__init__(**kwargs)
#
#     def build(self, input_shape):
#         # Create a trainable weight variable for this layer.
#         # self.kernel = self.add_weight(name='kernel',
#         #                               shape=(input_shape[1], self.output_dim),
#         #                               initializer='uniform',
#         #                               trainable=True)
#         super(Sample, self).build(input_shape)  # Be sure to call this somewhere!
#
#     def call(self, x, mask=None):
#
#         def __sample(preds, temperature=1.0):
#             # helper function to sample an index from a probability array
#             preds = np.asarray(preds).astype('float32')
#             preds = np.log(preds) / temperature
#             exp_preds = np.exp(preds)
#             preds = exp_preds / np.sum(exp_preds)
#             probas = np.random.multinomial(1, preds, 1)
#             return np.argmax(probas)
#
#         preds = K.eval(x)
#         print(preds)
#         domains = []
#         for j in range(preds.shape[0]):
#             word = []
#             for i in range(preds.shape[1]):
#                 word.append(__sample(preds[j][i]))
#             domains.append(word)
#
#         domains = np.ndarray(domains, dtype=int)
#         return K.variable(domains, dtype='int')
#
#     def compute_output_shape(self, input_shape):
#         return (input_shape[0], self.output_dim)


def sampling(preds):
    def __sample(preds, temperature=1.0):
        # helper function to sample an index from a probability array
        preds = np.asarray(preds).astype('float32')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    domains = []
    for j in range(preds.shape[0]):
        word = []
        for i in range(preds.shape[1]):
            word.append(__sample(preds[j][i]))
        domains.append(word)

    return domains


def sampling2(x):
    def __sample(preds, temperature=1.0):
        # helper function to sample an index from a probability array
        # preds = K.expand_dims(preds,axis=0)
        # print(preds)
        preds = K.log(preds) / temperature
        exp_preds = K.exp(preds)
        preds = exp_preds / K.sum(exp_preds)
        probas = np.random.multinomial(1, K.eval(preds), 1)
        return K.expand_dims(K.variable(np.argmax(probas)))

    batch_size = 2
    b = K.int_shape(x)[1]
    for i in range(1):
        result = __sample(x[i, 0, :])
        for j in range(b):
            if j == 0:
                continue
            c = __sample(x[i, j, :])
            result = K.concatenate([result, c], axis=0)


    return result


if __name__ == '__main__':
    from keras.models import Sequential, Model
    from keras.optimizers import RMSprop
    from keras.layers import Dense, Lambda, Input
    from keras import backend as K

    # set learning phase to 0
    K.set_learning_phase(0)
    tf_session = K.get_session()

    # kvar = K.variable(np.array([[1, 2], [3, 4]]), dtype='float32')
    # print K.print_tensor(kvar)
    # print(K.eval(kvar))


    # noise = np.random.normal(size=(2, 15,38))
    noise = K.random_uniform(shape=(2, 15, 38), maxval=1, minval=0, dtype="float32", seed=42)
    # print(noise.shape)
    # print(K.get_value(noise))
    import tensorflow as tf

    # in_plc = tf.placeholder(tf.float32, [None, 15,38], name="placeholder")
    inp = Input(tensor=noise, shape=(15, 38))
    exa = Lambda(lambda x: sampling2(x), output_shape=(15,))(inp)
    print(K.eval(exa))
    model = Model(inputs=inp, outputs=exa)
    #
    # model = Sequential()
    # model.add(Lambda(lambda x: call(x), output_shape=(15, 38), input_shape=(15, 38)))
    # optimizer = RMSprop(lr=0.01)
    # model.compile(loss='categorical_crossentropy', optimizer=optimizer)
    model.summary()
