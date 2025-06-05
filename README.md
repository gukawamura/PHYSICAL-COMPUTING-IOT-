# PHYSICAL-COMPUTING-IOT-

RM 550360  | Anna heloisa Soto Yagyu

RM 99275    | Breno da Silva Santos

RM 99679    | Gustavo Kawamura Christofani

# Sistema de Detecção de Pose com MediaPipe e Alertas

Este projeto utiliza a biblioteca MediaPipe da Google para detecção de pose em tempo real, integrando funcionalidades de alerta visual e sonoro (notificações do Windows) para luminosidade ambiente e um gesto de emergência (SOS) com os braços.

## 🌟 Funcionalidades

* **Detecção de Pose em Tempo Real:** Identifica e exibe os principais pontos (landmarks) do corpo humano através da câmera.
* **Alerta de Baixa Luminosidade:** Detecta e notifica o usuário quando o ambiente está com pouca luz, indicando uma possível necessidade de acender uma fonte de luz.
* **Detecção de Gesto SOS:** Reconhece um gesto específico (ambos os braços levantados acima da cabeça em forma de "Y") como um sinal de emergência, acionando um alerta visual na tela e uma notificação no sistema.
* **Notificações Desktop:** Utiliza o `win10toast` para enviar alertas pop-up nativos do Windows.

## 🛠️ Tecnologias Utilizadas

* **Python:** Linguagem de programação principal.
* **OpenCV (`cv2`):** Para captura de vídeo da câmera e manipulação de imagens.
* **MediaPipe (`mediapipe`):** Framework de ML para detecção de pose.
* **NumPy (`numpy`):** Para operações numéricas, especialmente no cálculo de brilho.
* **Win10toast (`win10toast`):** Para notificações pop-up no Windows.

## 🚀 Como Rodar o Projeto

Siga os passos abaixo para configurar e executar o projeto em seu ambiente.

### Pré-requisitos

* **Python 3.9 ou 3.10** (versões mais recentes como 3.11+ podem ter problemas de compatibilidade com o MediaPipe devido à disponibilidade de "wheels").

* **VS Code (Opcional, mas Recomendado):** Para uma experiência de desenvolvimento integrada.


### Instalação e Execução

1.  **Clone este repositório (ou baixe os arquivos):**
    ```bash
    git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)
    cd SEU_REPOSITORIO # Navegue até a pasta do projeto
    ```
    *Substitua `SEU_USUARIO` e `SEU_REPOSITORIO` pelos seus dados.*

2.  **Crie e Ative um Ambiente Virtual (Altamente Recomendado):**
    Isso isola as dependências do seu projeto, evitando conflitos.

    * **Criar o ambiente virtual:**
        ```bash
        python -m venv venv
        ```

    * **Ativar o ambiente virtual:**
        * **No Windows (PowerShell - padrão no VS Code):**
            ```powershell
            .\venv\Scripts\Activate.ps1
            ```
            * *Se você receber um erro sobre a execução de scripts (`ExecutionPolicy`), execute este comando no **PowerShell como Administrador** (apenas uma vez):*
                ```powershell
                Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
                ```
                * *Depois, feche o PowerShell Admin e tente ativar novamente no terminal do VS Code.*

        * **No Windows (Prompt de Comando - CMD):**
            ```cmd
            .\venv\Scripts\activate.bat
            ```
        * **No macOS/Linux:**
            ```bash
            source venv/bin/activate
            ```

    * Após a ativação, você verá `(venv)` no início da linha de comando, indicando que o ambiente virtual está ativo.

3.  **Instale as Dependências:**
    Com o ambiente virtual ativo, instale todas as bibliotecas necessárias:
    ```bash
    pip install opencv-python mediapipe numpy win10toast
    ```

4.  **Execute o Programa:**
    Com o ambiente virtual ainda ativo, execute o script principal:
    ```bash
    python app.py
    ```
    * (Se o nome do seu arquivo principal for diferente, substitua `app.py` pelo nome correto).

## 💡 Como Usar

* Ao iniciar o programa, uma janela de vídeo exibirá o feed da sua câmera.
* **Detecção de Pose:** O programa desenhará os pontos de referência do corpo sobre a sua imagem.
* **Alerta de Luminosidade:** Diminua a luz ambiente ou cubra a câmera para testar o alerta de baixa luminosidade. Uma notificação do Windows e/ou uma mensagem na tela pode aparecer.
* **Gesto SOS:** Levante ambos os braços esticados acima da cabeça, formando um formato de "Y" com seu corpo. O programa detectará o gesto e ativará o alerta.

## 🛑 Como Parar o Programa

* **Pressione a tecla `q`** (minúscula) enquanto a janela de vídeo estiver focada.
* Alternativamente, clique no terminal do VS Code e pressione **`Ctrl + C`**.

---
## 🛑 Vídeo Demonstrativo

https://youtu.be/d3s27DjZkXc
