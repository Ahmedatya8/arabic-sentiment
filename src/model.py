from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Input, Embedding, Bidirectional, LSTM,
    Dense, Dropout, SpatialDropout1D
)

def build_bilstm(vocab_size, embed_dim=128, lstm_units=64,
                 num_classes=3, max_len=50):
    inp = Input(shape=(max_len,))
    x   = Embedding(vocab_size, embed_dim, input_length=max_len)(inp)
    x   = SpatialDropout1D(0.3)(x)
    x   = Bidirectional(LSTM(lstm_units, return_sequences=True))(x)
    x   = Bidirectional(LSTM(lstm_units // 2))(x)
    x   = Dense(64, activation="relu")(x)
    x   = Dropout(0.4)(x)
    out = Dense(num_classes, activation="softmax")(x)
    model = Model(inp, out)
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model