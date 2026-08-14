# Physical AI 프로젝트 — MakerWorld RC Rover 개조 계획

## 1. 참고 모델

MakerWorld의 **RC Rover with Robot Arm 6-DOF** 모델을 기반으로 프로젝트를 진행한다.

원본 구성에 포함된 주요 부품:

- Arduino Mega ×1
- Arduino Uno ×1
- NRF24L01 무선 모듈 ×2
- NRF24L01 전원 어댑터 ×2
- 37mm 감속 DC 모터 ×2
- L298N 모터 드라이버 ×1
- MG996R 또는 MG995 서보 ×4
- MG90 서보 ×3
- 조이스틱 모듈 ×2
- 전위차계 ×2
- 토글 스위치 ×3
- 5mm LED 및 저항 ×5
- 미니 브레드보드 ×1
- LM2596 스텝다운 전압 레귤레이터 ×1
- 3S LiPo 배터리 ×1
- 18650 배터리 ×2
- 듀얼 배터리 홀더 ×1
- KCD1 로커 스위치 ×1
- 608 베어링 ×4
- 각종 M3/M8 볼트 및 너트

---

## 2. 내가 만들고 싶은 것

원본의 **2륜 구동 + 6-DOF 로봇팔 구조는 우선 그대로 사용**한다.

여기에 Physical AI 기능을 추가한다.

### 구동

- 모터에 **Encoder를 추가/적용**
- Encoder feedback을 이용한 모터 제어
- 모터 드라이버도 자율주행에 맞게 구성

### 컴퓨팅

- 기존 Arduino 중심 구조를 변경
- **ESP32를 저수준 제어용으로 사용**
- **Jetson을 고수준 AI/ROS 2 컴퓨터로 사용**

### 센서

- 카메라 추가
- IMU 추가
- 추후 필요하면 LiDAR 추가

### 자율주행

- ROS 2 기반으로 차량 제어
- Encoder와 센서 데이터를 이용한 주행
- 카메라를 이용한 주변/물체 인식
- 추후 SLAM 및 자율주행으로 확장

### 로봇팔

- 기존 6-DOF 로봇팔 사용
- ESP32를 통해 서보 제어
- Jetson에서 고수준 로봇팔 제어
- Action Message를 받아 로봇팔이 움직이도록 구성
- 장기적으로 물체를 인식하고 집거나 옮기는 기능까지 확장

---

## 3. 개발 방향

### V1

**기존 MakerWorld 2륜 구조를 그대로 사용**

```text
2WD Rover
   +
Encoder
   +
ESP32
   +
Jetson
   +
Camera / IMU
   +
6-DOF Robot Arm
   ↓
ROS 2 기반 Physical AI Rover
```

먼저 V1을 완성한 뒤 필요하면 직접 설계한 4륜 플랫폼으로 확장한다.

---

## 4. 최종 목표

```text
Camera / IMU / Encoder
          ↓
       Jetson
          ↓
     ROS 2 / AI
       ↙     ↘
  자율주행    Robot Arm
                 ↓
             Action 수행
```

**목표: 기존 2륜 RC Rover를 기반으로 자율주행과 로봇팔 조작이 가능한 Physical AI 플랫폼으로 개조한다.**
