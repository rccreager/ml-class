import tensorflow as tf
import wandb

# logging code
run = wandb.init()
config = run.config
config.epochs = 100
config.lr = 0.01
config.layers = 3
config.dropout = 0.4
config.hidden_layer_1_size = 128

# load data
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()

X_train = X_train / 255.
X_test = X_test / 255.

img_width = X_train.shape[1]
img_height = X_train.shape[2]
labels = ["T-shirt/top", "Trouser", "Pullover", "Dress",
          "Coat", "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]

# one hot encode outputs
y_train = tf.keras.utils.to_categorical(y_train)
y_test = tf.keras.utils.to_categorical(y_test)

num_classes = y_train.shape[1]

# create model
model = tf.keras.models.Sequential()
#model.add(Reshape((img_width, img_height, 1), input_shape=(img_width,img_height)))
model.add(tf.keras.layers.Flatten(input_shape=(img_width, img_height)))
model.add(tf.keras.layers.Dropout(config.dropout))
model.add(tf.keras.layers.Dense(config.hidden_layer_1_size, activation='relu'))
model.add(tf.keras.layers.Dropout(config.dropout))
model.add(tf.keras.layers.Dense(num_classes, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam',
              metrics=['accuracy'])
# Fit the model
model.fit(X_train, y_train, epochs=config.epochs, validation_data=(X_test, y_test),
          callbacks=[wandb.keras.WandbCallback(data_type="image", labels=labels)])
