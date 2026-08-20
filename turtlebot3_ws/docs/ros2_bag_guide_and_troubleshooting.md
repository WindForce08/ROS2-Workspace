# ROS 2 `ros2 bag` 사용 가이드 및 트러블슈팅

이 문서는 ROS 2에서 `ros2 bag` 명령어를 사용할 때 발생한 `[ERROR] [rosbag2_storage]: No storage id specified...` 오류의 원인과 복구 방법, 그리고 예방법을 정리한 안내서입니다.

---

## 1. 실행하려던 명령어의 개념 및 역할

`ros2 bag`은 ROS 2 네트워크에서 발행(Publish)되는 토픽 메시지 데이터를 파일로 **기록(Record)**하고, 나중에 필요할 때 동일한 시간 간격으로 **재생(Play)**할 수 있는 툴입니다.

### 실행한 명령어별 상세 설명

1. **`ros2 bag record /scan /image /tf`**
   - **기능**: 선택한 특정 토픽(`/scan`, `/image`, `/tf`)의 메시지만 선택하여 기록합니다.
   - **용도**: 센서 데이터 중 용량이 큰 카메라 데이터나 특정 센서/트랜스폼 데이터만 골라서 저장할 때 사용합니다.

2. **`ros2 bag record -a -o field_test_01`**
   - **기능**: 현재 ROS 2 네트워크 상에서 통신 중인 모든 토픽(`-a` 또는 `--all`)을 `field_test_01`이라는 지정된 폴더 이름(`-o`)으로 저장합니다.
   - **용도**: 실험이나 현장 테스트 시 전체 시스템 데이터를 한 번에 기록할 때 사용합니다.

3. **`ros2 bag play field_test_01`**
   - **기능**: `field_test_01` 폴더에 저장된 bag 데이터의 메시지들을 원래 기록된 타임스탬프에 맞춰 다시 ROS 2 토픽으로 재생(발행)합니다.
   - **용도**: 로봇이 없는 환경에서 과거 실험 데이터를 재현하여 노드를 테스트할 때 사용합니다.

4. **`ros2 bag info field_test_01`**
   - **기능**: `field_test_01` 폴더에 포함된 데이터의 개요(기록 시간, 메시지 총 개수, 저장된 토픽 목록 및 타입, 저장 포맷 등)를 요약하여 보여줍니다.

---

## 2. 발생한 오류의 원인 분석

### 발생한 오류 메시지
```bash
pa31@pa31-Legion-Pro-5-16IAX10:~/turtlebot3_ws$ ros2 bag play field_test_01

closing.

closing.
[ERROR] [1786670290.717247420] [rosbag2_storage]: No storage id specified, and no plugin found that could open URI
No storage could be initialized from the inputs.
```

### 핵심 원인: `metadata.yaml` 파일 누락
ROS 2의 `rosbag2` 시스템은 bag 저장 폴더 내에 두 종류의 파일이 포함되어야 작동합니다.
1. **데이터 파일**: `field_test_01_0.db3` (SQLite3 포맷 데이터베이스 파일)
2. **메타데이터 파일**: **`metadata.yaml`** (저장소 포맷인 `sqlite3`/`mcap`, 토픽 이름, 메세지 타입 등의 정보를 담은 설정 파일)

`ros2 bag record` 진행 시 메시지는 `.db3` 파일에 계속 기록되지만, **`metadata.yaml` 파일은 녹화가 정상적으로 종료(Tear down)되는 시점에 생성**됩니다.

녹화 도중 다음과 같은 상황이 발생하면 `metadata.yaml`이 쓰이지 않고 비정상 종료됩니다:
- 터미널 창을 강제로 닫음
- `kill -9` (SIGKILL) 프로세스 강제 종료
- 시스템 다운 또는 전원 차단

결과적으로 `ros2 bag play`나 `ros2 bag info`를 실행했을 때 **`metadata.yaml`이 없으므로** ROS 2는 해당 폴더가 어떤 저장소 구조(`sqlite3`인지 `mcap`인지)인지 파악하지 못해 **"No storage id specified..."** 오류를 출력하게 됩니다.

---

## 3. 에러 복구 방법 (이미 발생한 경우)

.db3 데이터베이스 파일 자체는 데이터(메시지)가 정상적으로 저장되어 있으므로, ROS 2의 **`reindex`** 기능을 통해 `metadata.yaml`을 자동으로 다시 생성(복구)할 수 있습니다.

### 복구 명령어
```bash
ros2 bag reindex -s sqlite3 field_test_01
```

### 복구 진행 과정 및 검증 (실제 적용 결과)
1. 복구 명령어 실행:
   ```bash
   ros2 bag reindex -s sqlite3 field_test_01
   # [INFO] [rosbag2_cpp]: Beginning reindexing bag in directory: field_test_01
   # [INFO] [rosbag2_storage]: Opened database 'field_test_01/field_test_01_0.db3' for READ_ONLY.
   # [INFO] [rosbag2_cpp]: Reindexing complete.
   ```
2. 복구 후 `ros2 bag info field_test_01` 확인 결과:
   - 총 206,903개의 메시지와 기록 시간(약 212초)이 정상 복구되어 `metadata.yaml`이 재작성되었습니다.
3. 이제 `ros2 bag play field_test_01`을 실행하면 정상적으로 재생됩니다.

---

## 4. 오류 예방법 및 올바른 사용 모범 사례

1. **녹화 정지 시 반드시 `Ctrl + C` (SIGINT) 사용**
   - `ros2 bag record`를 멈출 때는 터미널을 바로 닫거나 `kill -9`를 쓰지 말고, 반드시 키보드의 **`Ctrl + C`**를 눌러 프로그램이 `metadata.yaml`을 생성하고 파일 연결을 안전하게 닫을 때까지 기다려야 합니다.

2. **녹화 종료 후 파일 구조 확인**
   - 녹화가 끝나면 해당 bag 디렉토리 내에 아래와 같이 두 파일이 모두 잘 존재하는지 확인하세요.
     ```text
     field_test_01/
     ├── field_test_01_0.db3
     └── metadata.yaml
     ```

3. **비정상 종료가 의심될 때는 `reindex` 수행**
   - 만약 불가피하게 컴퓨터가 꺼지거나 강제 종료되어 `metadata.yaml`이 없어졌더라도 데이터 파일(`.db3`)이 남아있다면 당황하지 말고 `ros2 bag reindex -s sqlite3 <폴더명>`을 실행하여 복구하세요.

---

## 5. 요약 체크리스트

| 상황 | 원인 | 해결책 / 예방법 |
| :--- | :--- | :--- |
| `ros2 bag play` 시 `No storage id specified` 오류 | `metadata.yaml` 파일 누락 | `ros2 bag reindex -s sqlite3 <폴더명>` 실행 |
| `ros2 bag record` 종료 시 | 비정상 종료 (강제 종료) | 반드시 **`Ctrl + C`**로 종료하여 메타데이터 자동 작성 생성 유도 |
| bag 파일 상태 확인 | 정보 확인 필요 | `ros2 bag info <폴더명>` 으로 메세지 수 및 duration 검증 |
