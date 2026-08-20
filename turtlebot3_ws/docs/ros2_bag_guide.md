# ROS 2 Bag 사용 가이드 (ROS 2 Humble)

이 문서는 ROS 2(Humble) 환경에서 `ros2 bag`을 사용하는 순서별 가이드입니다.

---

## 0. ROS 2 환경 설정
터미널을 열고 ROS 2 환경을 로드합니다.
```bash
source /opt/ros/humble/setup.bash
```

---

## 1. rosbag 파일 정보 확인 (`info`)
재생하기 전에 bag 파일에 어떤 토픽과 데이터 타입이 들어있는지 확인합니다.
> **참고:** ROS 2의 bag은 단일 파일이 아니라 **폴더 형태**로 저장됩니다 (`metadata.yaml`과 `.db3` 또는 `.mcap` 파일이 들어있는 폴더).

```bash
ros2 bag info <bag_폴더_경로>
```
* **예시:**
  ```bash
  ros2 bag info my_bag_data
  ```

---

## 2. rosbag 재생하기 (`play`)

### ① 기본 재생
```bash
ros2 bag play <bag_폴더_경로>
```

### ② 자주 사용하는 재생 옵션
| 기능 | 명령어 옵션 | 설명 |
| :--- | :--- | :--- |
| **배속 조절** | `-r <속도>` | 예: 2배속 재생 `ros2 bag play my_bag_data -r 2.0` |
| **반복 재생** | `-l` 또는 `--loop` | 끝까지 재생 후 처음부터 다시 재생 |
| **특정 토픽만 재생** | `--topics <토픽1> <토픽2>` | 예: `ros2 bag play my_bag_data --topics /scan /cmd_vel` |
| **일시정지 상태로 시작** | `--start-paused` | 실행 후 `Space` 키를 눌러 재생/일시정지 전환 |
| **시뮬레이션 시간 발행** | `--clock` | `/clock` 토픽을 발행하여 RViz2 등과 시간 동기화 |

---

## 3. 재생 데이터 확인하기

`ros2 bag play`를 실행 중인 상태에서 **새 터미널**을 열어 토픽이 정상 발행되는지 확인합니다.

1. **활성화된 토픽 목록 확인**
   ```bash
   ros2 topic list
   ```
2. **특정 토픽 데이터 출력 확인**
   ```bash
   ros2 topic echo /scan
   ```
3. **시각화 툴 (RViz2) 실행**
   ```bash
   rviz2
   ```

---

## 4. 새로운 rosbag 데이터 기록하기 (`record`)

새로운 데이터를 직접 기록(녹화)하고 싶을 때는 아래 명령어를 사용합니다.

* **특정 토픽만 기록**:
  ```bash
  ros2 bag record /scan /cmd_vel -o 저장할_bag_폴더명
  ```
* **모든 토픽 기록**:
  ```bash
  ros2 bag record -a -o 저장할_bag_폴더명
  ```
  *(종료하려면 `Ctrl + C` 입력)*
