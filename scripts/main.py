import os
import cv2
import torch
import pyrender
import trimesh
import numpy as np

# Caminho absoluto até a pasta yolov5 clonada
YOLOV5_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'yolov5'))

# Carrega o modelo YOLOv5l a partir do repositório local
model = torch.hub.load(YOLOV5_PATH, 'yolov5m', source='local')

# Cria a cena da Realidade Aumentada
scene = pyrender.Scene()
viewer = pyrender.Viewer(scene, use_raymond_lighting=True, run_in_thread=True)

# Defina os índices das classes relevantes (livro, celular, etc.)
# 27 - bag (carteira), 57 - book (livro), 62 - remote (controle), 67 - cell phone (celular)
relevant_class_ids = [39, 41, 42, 43, 44, 45, 46, 47, 48, 53, 54, 55, 63, 64, 65, 66, 67, 73, 74, 76, 77, 79]  # Índices de classes de interesse

# Limiar de confiança para detecções
conf_threshold = 0.5  # Ajuste esse valor conforme necessário

# Função para exibir uma caixa 3D com informações sobre o objeto detectado
def show_info_box(label):
    # Criação de uma caixa 3D
    mesh = trimesh.creation.box(extents=(0.2, 0.1, 0.01), smooth=False)  # Definindo smooth=False

    # Aplicando cor ao mesh
    mesh.visual.face_colors = [100, 200, 255, 180]  # RGBA

    # Criando um material simples
    material = pyrender.MetallicRoughnessMaterial(
        baseColorFactor=[0.39, 0.78, 1.0, 1.0]  # Azul claro
    )

    # Convertendo o mesh para o formato do Pyrender e aplicando o material
    box_node = pyrender.Mesh.from_trimesh(mesh, material=material)
    scene.add(box_node)

    print(f"[INFO] Objeto detectado: {label}")

# Inicializa a webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Executa a detecção com o YOLOv5
    results = model(frame, size=640)  # Tamanho da imagem de entrada aumentado para melhor precisão
    detections = results.xyxy[0]  # Coordenadas e classes

    for *box, conf, cls in detections:
        if conf < conf_threshold:  # Ignora detecções abaixo do limiar de confiança
            continue
        
        x1, y1, x2, y2 = map(int, box)
        class_id = int(cls)
        label = results.names[class_id]

        # Desenha a caixa e o rótulo na imagem da webcam
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Exibe uma "caixa de informação RA" para certos objetos
        if class_id in relevant_class_ids:
            show_info_box(label)

    # Mostra o vídeo com as detecções
    cv2.imshow("Câmera", frame)

    # Sai com a tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Finaliza
cap.release()
cv2.destroyAllWindows()