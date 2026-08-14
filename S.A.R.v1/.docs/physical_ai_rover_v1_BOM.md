# Physical AI Rover V1 — BOM (Bill of Materials)

> **목적:** MakerWorld `RC Rover with Robot Arm 6-DOF`를 기구 베이스로 사용하고, PC + ROS 2 + ESP32 기반의 Physical AI Rover V1을 구성하기 위한 부품 비교용 BOM.
>
> **현재 설계 기준:** Jetson 제외. PC가 ROS 2/RViz2/AI/카메라 처리, ESP32가 모터·엔코더·서보 등 저수준 제어를 담당한다.
>
> **가격 원칙:** 가격은 변동되므로 구매 전 판매 페이지에서 다시 확인한다. `미확인`은 아직 특정 모델을 확정하지 않았거나 신뢰할 만한 현재 가격을 확인하지 않은 항목이다.
>
> **작성 기준일:** 2026-08-13

---

## 1. 프로젝트 기준 구성

```text
PC
├── ROS 2
├── RViz2
├── Camera / AI
└── High-level control
        │
        │ USB / Serial
        ▼
ESP32
├── DC Motor Control
├── Encoder Feedback
└── 6-DOF Servo Control
        │
        ├── 2WD Rover
        └── 6-DOF Robot Arm
```

### 제외 부품

- Jetson
- Arduino Mega
- Arduino Uno
- NRF24L01 무선 통신 모듈
- 조이스틱 기반 RC 송신부
- 전위차계
- 18650 ×2 기반 별도 전원계

---

# 2. 핵심 BOM

| ID | 분류 | 부품 | 수량 | 권장 사양/모델 | 제조사 | 현재 가격 | 구매/제품 링크 | 비교 상태 | 비고 |
|---|---|---|---:|---|---|---:|---|---|---|
| CTRL-01 | 제어 | ESP32 개발보드 | 1 | ESP32-DevKitC 계열 | Espressif | 확인 필요 | https://www.espressif.com/en/products/devkits/esp32-devkitc/overview | 🔎 비교 필요 | 저수준 제어기 |
| CTRL-02 | 제어 | 개발/통신용 USB 케이블 | 1~2 | ESP32 보드 호환 | - | 확인 필요 | - | 🔎 | PC ↔ ESP32 |
| DRIVE-01 | 구동 | 37mm 감속 DC 기어드모터 + Encoder | 2 | Encoder 내장형, 전압/전류/감속비 확정 필요 | 미정 | 확인 필요 | - | ⚠️ 선정 필요 | 핵심 구매품 |
| DRIVE-02 | 구동 | 듀얼 DC 모터 드라이버 | 1 | 모터 정격/스톨 전류에 맞게 선정 | 미정 | 확인 필요 | - | ⚠️ 선정 필요 | L298N은 일단 보류 |
| DRIVE-03 | 구동 | 구동 바퀴 | 2 | MakerWorld 원본 호환 | - | 확인 필요 | MakerWorld 원본 | 🔎 | 기구부 확인 |
| DRIVE-04 | 구동 | 608 베어링 | 4 | 608 규격 | 미정 | 확인 필요 | - | 🔎 | 원본 BOM |
| ARM-01 | 로봇팔 | 고토크 서보 | 4 | MG996R 또는 MG995 | Tower Pro/호환 | 3,160원/개 최저가 확인 | https://prod.danawa.com/info/?pcode=15141536 | 🔎 비교 필요 | 2026-08-13 확인 |
| ARM-02 | 로봇팔 | 소형 서보 | 3 | MG90S/MG90 계열 | 미정 | 확인 필요 | - | 🔎 비교 필요 | 원본 BOM |
| ARM-03 | 로봇팔 | Gripper | 1 | MakerWorld 원본 | - | 포함/제작 | MakerWorld 원본 | 🔎 | 원본 구조 사용 |
| POWER-01 | 전원 | 3S LiPo 배터리 | 1 | 용량/방전율은 모터 선정 후 결정 | 미정 | 확인 필요 | - | ⚠️ 선정 필요 | 메인 배터리 |
| POWER-02 | 전원 | LiPo 충전기 | 1 | 3S Balance Charger | 미정 | 확인 필요 | - | 🔎 | 배터리 확정 후 선정 |
| POWER-03 | 전원 | 메인 전원 스위치 | 1 | DC 고전류 대응 | 미정 | 확인 필요 | - | 🔎 | 메인 전원 차단 |
| POWER-04 | 전원 | 5V Buck Converter | 1 | 입력 3S LiPo 대응, ESP32 전원용 | 미정 | 11,890원 확인 | https://prod.danawa.com/info/?pcode=5059187 | 🔎 비교 필요 | LM2596 모듈 예시 |
| POWER-05 | 전원 | 5~6V 고전류 BEC | 1 | 7개 서보 동시 동작 고려 | 미정 | 확인 필요 | - | ⚠️ 선정 필요 | 서보 전원 |
| POWER-06 | 전원 | Fuse / 보호장치 | 1 set | 배터리/모터 전류에 맞게 선정 | 미정 | 확인 필요 | - | 🔎 | 안전 필수 |
| POWER-07 | 전원 | 전원 분배부 | 1 | XT 계열/터미널/분배보드 | 미정 | 확인 필요 | - | 🔎 | 전원 배선 |
| SENSOR-01 | 센서 | IMU | 1 | 6축 또는 9축 IMU | 미정 | 확인 필요 | - | 🔎 비교 필요 | `/imu/data` |
| SENSOR-02 | 센서 | USB Camera | 1 | FHD 1080p 이상 | Logitech 등 | 76,250원 확인(C920 병행수입) | https://prod.danawa.com/info/?pcode=7346617 | 🔎 비교 필요 | 초기 PC 연결용 |
| MECH-01 | 기구 | Rover chassis 3D print | 1 set | MakerWorld 원본 | MakerWorld | 제작비 별도 | https://makerworld.com/ko/models/1342319-rc-rover-with-robot-arm-6-dof#profileId-1383072 | 🔎 | 원본 기구부 |
| MECH-02 | 기구 | 6-DOF Arm 3D print | 1 set | MakerWorld 원본 | MakerWorld | 제작비 별도 | https://makerworld.com/ko/models/1342319-rc-rover-with-robot-arm-6-dof#profileId-1383072 | 🔎 | 원본 기구부 |
| MECH-03 | 체결 | M3/M8 볼트·너트 | 1 set | 원본 규격 기준 | 미정 | 확인 필요 | - | 🔎 | 조립용 |
| WIRE-01 | 배선 | 전원선/신호선/커넥터 | 1 set | 모터 전류에 맞는 규격 | 미정 | 확인 필요 | - | 🔎 | 제작 환경에 따라 변동 |

---

# 3. 제조사 / 판매처 비교표

구매 후보를 조사할 때 아래 표를 채운다.

| BOM ID | 품목 | 후보 A 제조사/판매처 | 링크 | 가격 | 후보 B 제조사/판매처 | 링크 | 가격 | 후보 C 제조사/판매처 | 링크 | 가격 | 선택 |
|---|---|---|---|---:|---|---|---:|---|---|---:|---|
| CTRL-01 | ESP32 |  |  |  |  |  |  |  |  |  |  |
| DRIVE-01 | Encoder 기어드모터 |  |  |  |  |  |  |  |  |  |  |
| DRIVE-02 | 모터 드라이버 |  |  |  |  |  |  |  |  |  |  |
| ARM-01 | MG996R/MG995 |  |  |  |  |  |  |  |  |  |  |
| ARM-02 | MG90S |  |  |  |  |  |  |  |  |  |  |
| POWER-01 | 3S LiPo |  |  |  |  |  |  |  |  |  |  |
| POWER-04 | 5V Buck |  |  |  |  |  |  |  |  |  |  |
| POWER-05 | 고전류 BEC |  |  |  |  |  |  |  |  |  |  |
| SENSOR-01 | IMU |  |  |  |  |  |  |  |  |  |  |
| SENSOR-02 | USB Camera |  |  |  |  |  |  |  |  |  |  |

---

# 4. 부품 선정 시 반드시 비교할 사양

## 4.1 Encoder Gear Motor

가격보다 아래 항목을 우선 비교한다.

| 항목 | 목표/확인값 |
|---|---|
| 정격 전압 | 확인 필요 |
| 정격 RPM | 확인 필요 |
| 감속비 | 확인 필요 |
| 정격 전류 | 확인 필요 |
| Stall Current | **필수 확인** |
| Encoder 방식 | Hall / Magnetic / Optical |
| Encoder PPR/CPR | **필수 확인** |
| 출력축 직경 | MakerWorld 기구부와 호환 |
| 출력축 형상 | D-cut 등 |
| 모터 크기 | 37mm 계열 |
| 가격 | 비교 |

> **모터를 먼저 확정한 후 Motor Driver, 배터리, BEC 용량을 결정한다.**

---

## 4.2 Motor Driver

| 항목 | 확인값 |
|---|---|
| 채널 수 | 2 |
| 모터 전압 | 모터와 일치 |
| 연속 출력 전류 | 모터 정격전류 이상 |
| Peak/Stall 전류 대응 | **필수** |
| PWM 입력 | ESP32 호환 |
| 방향 제어 | H-Bridge |
| 과전류 보호 | 권장 |
| 과열 보호 | 권장 |
| 가격 | 비교 |

> **L298N은 원본 BOM에 포함되어 있지만 최종 V1 부품으로 확정하지 않는다.**

---

## 4.3 Servo / BEC

7개의 서보를 사용하므로 단순히 "서보 7개 × 평균전류"로 결정하지 않는다.

| 항목 | 확인값 |
|---|---|
| MG996R/MG995 수량 | 4 |
| MG90S 수량 | 3 |
| 동작 전압 | 확인 |
| Stall Current | 확인 |
| BEC 출력전류 | 선정 필요 |
| BEC 출력전압 | 5~6V 범위 검토 |
| Servo Power Distribution | 필요 |
| GND 공통 연결 | 필요 |

---

# 5. 현재 확인된 가격

> 아래 가격은 2026-08-13 검색 시점의 참고값이며 배송비/옵션/판매처에 따라 달라질 수 있다.

| 품목 | 모델 | 확인 가격 | 출처 |
|---|---|---:|---|
| MG996R | 180도 서보 | **3,160원/개 최저가** | 다나와 |
| LM2596 | 5A Step-down 모듈 | **11,890원** | 다나와 |
| Logitech C920 | FHD USB Camera | **76,250원** | 다나와 |

### 참고 링크

- ESP32-DevKitC 공식 제품/구매 정보: https://www.espressif.com/en/products/devkits/esp32
- ESP32-DevKitC 공식 문서: https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/index.html
- MG996R 가격비교: https://prod.danawa.com/info/?pcode=15141536
- LM2596 가격비교: https://prod.danawa.com/info/?pcode=5059187
- Logitech C920 가격비교: https://prod.danawa.com/info/?pcode=7346617
- MakerWorld 원본 모델: https://makerworld.com/ko/models/1342319-rc-rover-with-robot-arm-6-dof#profileId-1383072

---

# 6. 구매 우선순위

## 1차 — 기구부 확인

- [ ] MakerWorld 3D print 부품
- [ ] 37mm Encoder 기어드모터 후보 선정
- [ ] Wheel / Shaft 호환성 확인
- [ ] Arm Servo 규격 확인

## 2차 — 전원/구동계

- [ ] Motor Driver 선정
- [ ] 3S LiPo 선정
- [ ] 5V Buck 선정
- [ ] Servo BEC 선정
- [ ] Fuse / Power Distribution 선정

## 3차 — 제어/센서

- [ ] ESP32 선정
- [ ] IMU 선정
- [ ] USB Camera 선정
- [ ] 배선/커넥터 선정

---

# 7. 제외 / 보류 목록

| 부품 | 상태 | 이유 |
|---|---|---|
| Jetson | ❌ 제외 | V1에서는 PC 사용 |
| Arduino Mega | ❌ 제외 | ESP32로 대체 |
| Arduino Uno | ❌ 제외 | ESP32로 대체 |
| NRF24L01 ×2 | ❌ 제외 | PC ↔ ESP32 구조 |
| Joystick ×2 | ❌ 제외 | ROS 2 기반 제어 |
| Potentiometer ×2 | ❌ 제외 | 원본 RC 입력용 |
| 18650 ×2 | ❌ 제외 | 전원 구조 단순화 |
| L298N | ⚠️ 보류 | 모터 전류 확인 후 결정 |

---

# 8. 최종 시스템의 전원 구조

```text
                    3S LiPo
                       │
                Main Power Switch
                       │
             ┌─────────┼─────────┐
             │         │         │
             ▼         ▼         ▼
       Motor Driver  5V Buck   5~6V BEC
             │         │         │
             ▼         ▼         ▼
         DC Motors   ESP32      Servos
             │
             ▼
          Encoder
             │
             └────────→ ESP32
```

---

# 9. 최종 ROS 2 시스템과 BOM 대응

```text
PC
│
├── ROS 2
│   ├── /cmd_vel
│   ├── /odom
│   ├── /joint_states
│   ├── /imu/data
│   ├── /camera/image_raw
│   └── Arm Action
│
└──────── USB / Serial ────────┐
                               ▼
                             ESP32
                               │
                    ┌──────────┼──────────┐
                    ▼          ▼          ▼
                  Motor     Encoder     Servo
                    │                     │
                  2WD Rover           6-DOF Arm
```

---

## 10. 참고 자료

- 프로젝트 계획 파일: `physical_ai_project_short_plan (1).md`
- 원본 모델: MakerWorld `RC Rover with Robot Arm 6-DOF`
- ESP32: Espressif ESP32 DevKits
- 가격 비교: Danawa

