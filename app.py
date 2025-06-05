import cv2
import mediapipe as mp
import numpy as np # Importar numpy para calcular o brilho
from win10toast import ToastNotifier # Importar para notificações do Windows
import time

# --- Funções Adicionais ---

# Função para calcular brilho médio do frame
def calcular_brilho(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return np.mean(gray)

# Função para detectar o gesto de braços em "Y" (SOS)
def detectar_bracos_em_Y(landmarks, image_width, image_height):
    # Índices dos landmarks do MediaPipe para partes do corpo relevantes
    RIGHT_SHOULDER = 12
    RIGHT_ELBOW = 14
    RIGHT_WRIST = 16
    LEFT_SHOULDER = 11
    LEFT_ELBOW = 13
    LEFT_WRIST = 15

    # Obter coordenadas dos landmarks (normalizadas de 0 a 1, então multiplicar por dimensão da imagem)
    try:
        rs_y = landmarks[RIGHT_SHOULDER].y * image_height
        re_y = landmarks[RIGHT_ELBOW].y * image_height
        rw_y = landmarks[RIGHT_WRIST].y * image_height

        ls_y = landmarks[LEFT_SHOULDER].y * image_height
        le_y = landmarks[LEFT_ELBOW].y * image_height
        lw_y = landmarks[LEFT_WRIST].y * image_height
    except IndexError:
        # Se algum landmark não for detectado, retorne False
        return False

    # Lógica para detectar braços levantados em 'Y':
    # O pulso e o cotovelo devem estar acima do ombro correspondente (menor valor Y na imagem)
    right_arm_up = rw_y < rs_y and re_y < rs_y
    left_arm_up = lw_y < ls_y and le_y < ls_y

    # Verifique se ambos os braços estão levantados
    return right_arm_up and left_arm_up

# --- Inicialização ---

# Inicializa a solução de pose do Mediapipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Inicializa o ToastNotifier para notificações no Windows
toaster = ToastNotifier()
# Variáveis de controle para evitar alertas repetitivos
alert_shown_brilho = False
alert_shown_gesto = False
last_alert_time_brilho = 0
last_alert_time_gesto = 0
ALERT_COOLDOWN = 10 # Tempo em segundos entre alertas para o mesmo tipo

# Inicia a captura de vídeo
cap = cv2.VideoCapture(0) # Usa a câmera integrada do computador/notebook (índice 0 é o mais comum)
if not cap.isOpened():
    print("Erro ao abrir a câmera. Verifique se ela está conectada e disponível.")
    exit()

print("Monitorando brilho e gesto SOS - Pressione 'q' na janela de vídeo para sair.")

# --- Loop Principal ---
while True:
    ret, frame = cap.read()
    if not ret:
        print("Falha ao capturar frame do vídeo. Encerrando.")
        break

    # --- Cálculo de Brilho ---
    brilho = calcular_brilho(frame)
    print(f"Brilho atual: {brilho:.2f}")

    # Limiar de brilho baixo (ajuste este valor conforme necessário)
    BRILHO_LIMIAR = 30 # Um valor baixo para indicar pouca luz

    if brilho < BRILHO_LIMIAR:
        current_time = time.time()
        if not alert_shown_brilho or (current_time - last_alert_time_brilho > ALERT_COOLDOWN):
            toaster.show_toast("Alerta de Ambiente", "Luminosidade muito baixa detectada!", duration=5, icon_path=None)
            alert_shown_brilho = True
            last_alert_time_brilho = current_time
    else:
        alert_shown_brilho = False # Resetar o alerta quando a luz voltar ao normal

    # --- Processamento de Pose com MediaPipe ---
    # Converter para RGB (Mediapipe prefere RGB)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgb.flags.writeable = False # Otimização: tornar a imagem não-escrevível para passar para o MediaPipe

    results = pose.process(rgb)

    rgb.flags.writeable = True # Tornar a imagem escrevível novamente para desenhar nela
    # frame = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR) # Se você quiser converter de volta para BGR

    # Se os landmarks da pose forem detectados, desenhe-os e exiba as posições
    if results.pose_landmarks:
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        h, w, _ = frame.shape
        landmarks = results.pose_landmarks.landmark

        # --- Detecção de Gesto SOS ---
        if detectar_bracos_em_Y(landmarks, w, h):
            cv2.putText(frame, 'GESTO SOS DETECTADO!', (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            current_time = time.time()
            if not alert_shown_gesto or (current_time - last_alert_time_gesto > ALERT_COOLDOWN):
                toaster.show_toast("Alerta de Emergência", "Gesto SOS detectado!", duration=5, icon_path=None)
                alert_shown_gesto = True
                last_alert_time_gesto = current_time
        else:
            alert_shown_gesto = False # Resetar o alerta quando o gesto não estiver mais presente

        # --- Exibição de Coordenadas (como no seu código original) ---
        try: # Usar try-except para evitar erros se landmarks específicos não forem detectados
            # Cabeça: usando o nariz (índice 0)
            head = landmarks[mp_pose.PoseLandmark.NOSE.value]
            head_coords = (int(head.x * w), int(head.y * h))
            cv2.putText(frame, f"Head: {head_coords}", (head_coords[0], head_coords[1] - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

            # Mão esquerda: usando o pulso esquerdo (índice 15)
            left_hand = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
            left_hand_coords = (int(left_hand.x * w), int(left_hand.y * h))
            cv2.putText(frame, f"L.Hand: {left_hand_coords}", (left_hand_coords[0], left_hand_coords[1] - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

            # Mão direita: usando o pulso direito (índice 16)
            right_hand = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
            right_hand_coords = (int(right_hand.x * w), int(right_hand.y * h))
            cv2.putText(frame, f"R.Hand: {right_hand_coords}", (right_hand_coords[0], right_hand_coords[1] - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

            # Pé esquerdo: usando o tornozelo esquerdo (índice 27)
            left_foot = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
            left_foot_coords = (int(left_foot.x * w), int(left_foot.y * h))
            cv2.putText(frame, f"L.Foot: {left_foot_coords}", (left_foot_coords[0], left_foot_coords[1] - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

            # Pé direito: usando o tornozelo direito (índice 28)
            right_foot = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
            right_foot_coords = (int(right_foot.x * w), int(right_foot.y * h))
            cv2.putText(frame, f"R.Foot: {right_foot_coords}", (right_foot_coords[0], right_foot_coords[1] - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        except Exception as e:
            # print(f"Erro ao acessar landmarks: {e}") # Descomente para depuração
            pass # Ignora se algum landmark específico não for encontrado

    # Exibe o frame
    cv2.imshow("Pose Estimation & Alerts", frame)

    # Encerra o loop ao pressionar a tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos
cap.release()
cv2.destroyAllWindows()
print("Monitoramento encerrado.")