import tensorflow as tf
from tensorflow.keras.applications import ResNet50, EfficientNetB0, VGG16
from tensorflow.keras import layers, Model
import numpy as np

class TransferLearningModel:
    def __init__(self, num_classes=10, img_size=(224, 224), model_type='resnet50'):
        self.num_classes = num_classes
        self.img_size = img_size
        self.model_type = model_type
        self.model = None
    
    def build_transfer_model(self, trainable_layers=0):
        """Build transfer learning model"""
        # Base model selection
        if self.model_type == 'resnet50':
            base_model = ResNet50(weights='imagenet', include_top=False, 
                                input_shape=(*self.img_size, 3))
        elif self.model_type == 'efficientnet':
            base_model = EfficientNetB0(weights='imagenet', include_top=False,
                                      input_shape=(*self.img_size, 3))
        elif self.model_type == 'vgg16':
            base_model = VGG16(weights='imagenet', include_top=False,
                             input_shape=(*self.img_size, 3))
        
        # Freeze base model layers
        base_model.trainable = False
        
        # Unfreeze top layers if specified
        if trainable_layers > 0:
            base_model.trainable = True
            for layer in base_model.layers[:-trainable_layers]:
                layer.trainable = False
        
        # Add custom head
        inputs = tf.keras.Input(shape=(*self.img_size, 3))
        x = base_model(inputs, training=False)
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dropout(0.3)(x)
        x = layers.Dense(512, activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.5)(x)
        x = layers.Dense(256, activation='relu')(x)
        x = layers.Dropout(0.3)(x)
        outputs = layers.Dense(self.num_classes, activation='softmax')(x)
        
        self.model = Model(inputs, outputs)
        
        # Compile with different learning rates for base and head
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return self.model
    
    def fine_tune(self, trainable_layers=20):
        """Fine-tune the model by unfreezing top layers"""
        base_model = self.model.layers[1]
        base_model.trainable = True
        
        # Freeze all layers except top ones
        for layer in base_model.layers[:-trainable_layers]:
            layer.trainable = False
        
        # Recompile with lower learning rate
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.00001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return self.model