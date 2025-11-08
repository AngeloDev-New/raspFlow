## 🧠 RaspFlow — Horus Eye

O **RaspFlow Horus Eye** é um protótipo que transforma um **Raspberry Pi** com **webcam** em um dispositivo inteligente capaz de **coletar imagens, treinar modelos e controlar fluxos de visão computacional** diretamente pelo **celular**.

> A proposta é simples: ligue o Raspberry, conecte-se via Bluetooth, configure a rede Wi-Fi, escolha (ou crie) um modelo de IA, e comece a operar — tudo na palma da sua mão.

---

### 🚀 Visão Geral

O **Horus Eye** é um MVP (Minimum Viable Product) que visa criar uma plataforma acessível para experimentos e automações de visão computacional em campo, utilizando recursos locais (Raspberry Pi) e/ou remotos (nuvem).

Ele foi idealizado para facilitar a configuração e o uso de modelos de IA embarcados sem depender de terminais ou interfaces complexas.

---

### ⚙️ Fluxo de Operação

1. **Inicialização**

   * Ao ser ligado, o Raspberry Pi ativa o serviço **RaspFlow Core**.
   * O serviço habilita o **Bluetooth** e entra em modo de descoberta.

2. **Emparelhamento**

   * O aplicativo móvel **Horus App** detecta o Raspberry próximo e solicita o emparelhamento.
   * Após conectado, o app exibe as **redes Wi-Fi disponíveis**.

3. **Configuração de Rede**

   * Pelo app, o usuário seleciona uma rede Wi-Fi e conecta o Raspberry à Internet.

4. **Seleção de Modelo**

   * O usuário pode:

     * Escolher um **modelo pré-treinado** (por exemplo, YOLO, MobileNet, ResNet, etc.);
     * Ou **criar um novo dataset** e treinar do zero (localmente ou via nuvem).

5. **Processamento e Controle**

   * O Horus Eye começa a capturar imagens, processá-las e executar ações ou fluxos definidos (ex: detecção de objetos, reconhecimento de estágios, etc.).

6. **Treinamento em Nuvem (Opcional)**

   * Para cenários de baixa capacidade de processamento no Raspberry, é possível integrar com um **serviço de computação em nuvem** (Horus Cloud) para realizar o treinamento de modelos e sincronizar resultados automaticamente.

---

### 🧩 Arquitetura do Sistema

```
+------------------+
|     Horus App    |  ←→  Interface Móvel (Bluetooth / Wi-Fi)
+------------------+
          ↓
+------------------+
|  RaspFlow Core   |  ←→  Controle local / Captura de imagens
| (Raspberry Pi)   |
+------------------+
          ↓
+------------------+
|   Horus Cloud    |  ←→  Treinamento e processamento remoto
+------------------+
```

---

### 📱 Funcionalidades do App

* 🔍 Descoberta automática do Raspberry via Bluetooth
* 🌐 Configuração de rede Wi-Fi
* 🧠 Seleção ou criação de modelos de IA
* 📸 Visualização de streaming da câmera
* ☁️ Opção de treinar e sincronizar datasets com a nuvem
* 🧰 Ferramentas para anotação e pré-processamento de imagens

---

### 🧰 Tecnologias Envolvidas

| Camada                 | Tecnologias                                         |
| ---------------------- | --------------------------------------------------- |
| **Dispositivo (Edge)** | Raspberry Pi, Python, OpenCV, Torch/TensorFlow Lite |
| **Mobile App**         | Flutter ou React Native (Bluetooth + Wi-Fi Setup)   |
| **Serviços de Nuvem**  | FastAPI / Flask + PyTorch / TensorFlow + Storage S3 |
| **Comunicação**        | Bluetooth RFCOMM, WebSocket, REST API               |
| **IA / Visão**         | YOLOv8, ResNet, MobileNet, Custom CNNs              |

---

### 💡 Casos de Uso

* Controle e monitoramento de experimentos agrícolas (ex: estágios de soja 🌱)
* Detecção de anomalias ou lesões em animais 🐷
* Inspeção automatizada em ambientes industriais 🏭
* Monitoramento remoto com IA embarcada 📹

---

### 🧠 Futuro e Expansões

* Integração com **Edge TPU** (Google Coral)
* **Sincronização contínua** com dashboards na nuvem
* **Atualizações OTA (Over-The-Air)** via app
* Módulo de **treinamento colaborativo (Federated Learning)**

---

### 🧪 Status do Projeto

🟢 **MVP em desenvolvimento**

* [x] Comunicação Bluetooth inicial
* [x] Interface básica do app
* [ ] Configuração Wi-Fi via app
* [ ] Escolha de modelo e upload de dataset
* [ ] Treinamento remoto integrado
* [ ] Dashboard na nuvem

---

### 🛠️ Como Executar (Protótipo)

```bash
# No Raspberry Pi
git clone https://github.com/AngeloDev-New/raspFlow.git
cd raspflow-horus-eye
pip install -r requirements.txt
python main.py
```

No aplicativo móvel:

1. Abra o **Horus App**
2. Detecte o Raspberry via Bluetooth
3. Configure o Wi-Fi
4. Escolha o modelo ou inicie o treinamento

---

### 📄 Licença

MIT License © 2025 — RaspFlow Project
Desenvolvido com 💚 por AngeloDev
