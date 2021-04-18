from transformers import AutoTokenizer, TFAutoModel
import numpy as np
# from tf.keras.preprocessing.sequence import pad_sequences
# from keras.utils.np_utils import to_categorical
import tensorflow as tf
import os
import configparser
class Intent_Cls:
    def __init__(self):
        checkpoint_path = "/home/vanhocvp/Code/SmartCall/training/api/model/checkpoints/training_1/cp.ckpt"
        checkpoint_dir = os.path.dirname(checkpoint_path)
        self.tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base", use_fast=False)
        self.model = self.creat_model(checkpoint_path)
        config = configparser.ConfigParser()
        config.read('/home/vanhocvp/Code/SmartCall/training/api/model/config.ini')
        # self.intent_list = config.get('DEFAULT','intent').split(',\n')
        self.intent_list = {0: 'cant_hear', 1: 'dont_clear', 2: 'all_field', 3: 'only_home', 4: 'provide_name', 5: 'provide_address'}
        print (self.intent_list)

    def creat_model(self, checkpoint_dir):
        phobert = TFAutoModel.from_pretrained("vinai/phobert-base")
        MAX_LEN = 30
        ids = tf.keras.layers.Input(shape=(30), dtype=tf.int32)
        mask = tf.keras.layers.Input(shape=(30,), name='attention_mask', dtype='int32')
        # For transformers v4.x+: 

        embeddings = phobert(ids,attention_mask = mask)[0]
        X =tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(256))(embeddings)
        y = tf.keras.layers.Dense(6, activation='softmax', name='outputs')(X)
        model = tf.keras.models.Model(inputs=[ids,mask], outputs=[y])
        model.summary()
        model.layers[2].trainable = False
        model.compile(optimizer='Adam',loss = 'categorical_crossentropy',metrics='accuracy')
        #### LOAD WEIGHT ###
        latest = tf.train.latest_checkpoint(checkpoint_dir)
        model.load_weights(checkpoint_dir)
        return model
    def encoding(self, sent,max_length = 30):
        all_sent = []
        all_mask_sent = []
        sent = [sent]
        for line in sent:
            line = line.lower()
            tokens = self.tokenizer.encode_plus(line, max_length=max_length,
                                        truncation=True, padding='max_length',
                                        add_special_tokens=True, return_attention_mask=True,
                                        return_token_type_ids=False, return_tensors='tf')
            umk = np.array(tokens['input_ids']).reshape(-1)
            mk = np.array(tokens['attention_mask']).reshape(-1)
            all_sent.append(umk)
            all_mask_sent.append(mk)

        all_sent = self.padding(all_sent,max_length=max_length)
        all_mask_sent = self.padding(all_mask_sent,max_length=max_length)
        all_sent = np.array(all_sent)
        all_mask_sent = np.array(all_mask_sent)
        return all_sent,all_mask_sent
    def padding(self, encoded, max_length):
        return tf.keras.preprocessing.sequence.pad_sequences(encoded,30,padding = 'post') 
    def get_intent(self, mess):
        x = self.encoding(mess)
        pred = self.model.predict(x)
        index = np.argmax(pred)
        return self.intent_list[index], pred[0][index]

# x = Intent_Cls()
# text  = ["cả khu đường 14 đường ông ích khiêm quận phúc lợi",
#         "gì cơ em",
#         "mình hông rõ lắm",
#         "quanh các khu đây đều không mất điện chỉ nhà mình chẳng có điện",
#         "tôi đang mất điện đường mười bảy đường cầu noi quận đại mỗ",
#         "tên ông là nguyễn đức cảnh nha",
#         "ngay mai di hoc ca ngay"]
# for i in text:
#     pre, score = x.get_intent(i)
#     print (pre, '\t', score,'\t', i)