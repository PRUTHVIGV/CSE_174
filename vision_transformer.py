import tensorflow as tf
import numpy as np
from tensorflow.keras import layers
import tensorflow_addons as tfa

class VisionTransformer:
    def __init__(self, image_size=224, patch_size=16, num_classes=10, d_model=768, num_heads=12, num_layers=12):
        self.image_size = image_size
        self.patch_size = patch_size
        self.num_patches = (image_size // patch_size) ** 2
        self.num_classes = num_classes
        self.d_model = d_model
        self.num_heads = num_heads
        self.num_layers = num_layers
    
    def create_patches(self, images):
        batch_size = tf.shape(images)[0]
        patches = tf.image.extract_patches(
            images=images,
            sizes=[1, self.patch_size, self.patch_size, 1],
            strides=[1, self.patch_size, self.patch_size, 1],
            rates=[1, 1, 1, 1],
            padding="VALID",
        )
        patches = tf.reshape(patches, [batch_size, self.num_patches, self.patch_size * self.patch_size * 3])
        return patches
    
    def patch_encoder(self, num_patches, projection_dim):
        return tf.keras.Sequential([
            layers.Dense(projection_dim),
            layers.Embedding(input_dim=num_patches, output_dim=projection_dim),
        ])
    
    def mlp(self, x, hidden_units, dropout_rate):
        for units in hidden_units:
            x = layers.Dense(units, activation=tf.nn.gelu)(x)
            x = layers.Dropout(dropout_rate)(x)
        return x
    
    def build_vit(self):
        inputs = layers.Input(shape=(self.image_size, self.image_size, 3))
        
        # Create patches
        patches = layers.Lambda(self.create_patches)(inputs)
        
        # Encode patches
        encoded_patches = layers.Dense(self.d_model)(patches)
        
        # Add positional embedding
        positions = tf.range(start=0, limit=self.num_patches, delta=1)
        position_embedding = layers.Embedding(input_dim=self.num_patches, output_dim=self.d_model)(positions)
        encoded_patches += position_embedding
        
        # Transformer blocks
        for _ in range(self.num_layers):
            # Layer normalization 1
            x1 = layers.LayerNormalization(epsilon=1e-6)(encoded_patches)
            
            # Multi-head attention
            attention_output = layers.MultiHeadAttention(
                num_heads=self.num_heads, key_dim=self.d_model // self.num_heads, dropout=0.1
            )(x1, x1)
            
            # Skip connection 1
            x2 = layers.Add()([attention_output, encoded_patches])
            
            # Layer normalization 2
            x3 = layers.LayerNormalization(epsilon=1e-6)(x2)
            
            # MLP
            x3 = self.mlp(x3, hidden_units=[self.d_model * 2, self.d_model], dropout_rate=0.1)
            
            # Skip connection 2
            encoded_patches = layers.Add()([x3, x2])
        
        # Final layer normalization
        representation = layers.LayerNormalization(epsilon=1e-6)(encoded_patches)
        
        # Global average pooling
        representation = layers.GlobalAveragePooling1D()(representation)
        
        # Dropout
        representation = layers.Dropout(0.5)(representation)
        
        # Classification head
        logits = layers.Dense(self.num_classes)(representation)
        
        model = tf.keras.Model(inputs=inputs, outputs=logits)
        return model

class EfficientViT:
    def __init__(self, num_classes=10):
        self.num_classes = num_classes
    
    def build_efficient_vit(self):
        """Lightweight ViT for mobile deployment"""
        inputs = layers.Input(shape=(224, 224, 3))
        
        # Patch embedding with smaller patches
        x = layers.Conv2D(384, kernel_size=16, strides=16, padding='valid')(inputs)
        x = layers.Reshape((-1, 384))(x)
        
        # Positional embedding
        seq_len = x.shape[1]
        pos_emb = layers.Embedding(seq_len, 384)(tf.range(seq_len))
        x = x + pos_emb
        
        # Lightweight transformer blocks
        for _ in range(6):
            # Attention
            attn = layers.MultiHeadAttention(num_heads=6, key_dim=64)(x, x)
            x = layers.Add()([x, attn])
            x = layers.LayerNormalization()(x)
            
            # FFN
            ffn = layers.Dense(768, activation='gelu')(x)
            ffn = layers.Dense(384)(ffn)
            x = layers.Add()([x, ffn])
            x = layers.LayerNormalization()(x)
        
        # Classification
        x = layers.GlobalAveragePooling1D()(x)
        x = layers.Dense(self.num_classes, activation='softmax')(x)
        
        return tf.keras.Model(inputs, x)

def train_vit(X_train, y_train, X_val, y_val):
    vit = VisionTransformer()
    model = vit.build_vit()
    
    model.compile(
        optimizer=tfa.optimizers.AdamW(learning_rate=0.001, weight_decay=0.0001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    callbacks = [
        tf.keras.callbacks.ReduceLROnPlateau(patience=5, factor=0.5),
        tf.keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)
    ]
    
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=100,
        batch_size=16,
        callbacks=callbacks
    )
    
    return model, history