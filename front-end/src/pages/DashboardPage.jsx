import React, { useState, useEffect, useRef } from 'react'; // useRef 추가
import apiClient from '../api/client';
import styles from './DashboardPage.module.css';

function DashboardPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  
  // 숨겨진 file input에 접근하기 위한 ref 생성
  const fileInputRef = useRef(null);

  const fetchData = async () => {
    // 데이터 로딩 중 상태를 다시 활성화 (업로드 후 새로고침 시)
    setLoading(true);
    try {
      const userId = localStorage.getItem('user_id'); // 로그인 시 저장된 user_id
      const response = await apiClient.get(`/v1/dashboard/today?user_id=${userId}`);
      setData(response.data);
    } catch (error) {
      console.error("데이터 로딩 실패", error);
      // 실패 시 기존 데이터는 유지하거나 null로 설정할 수 있습니다.
      setData(null); 
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);
  
  // + 버튼 클릭 시 실행될 핸들러
  const handleAddClick = () => {
    // 숨겨진 file input을 클릭
    fileInputRef.current.click();
  };

// DashboardPage.jsx

  // 파일이 선택되었을 때 실행될 핸들러
  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      // ===== 1단계: 이미지 업로드 및 AI로 음식 이름 분석 =====
      alert('이미지를 분석합니다...');
      const uploadResponse = await apiClient.post('/v1/food/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      
      const recognizedFoodName = uploadResponse.data.food_name;
      if (!recognizedFoodName) {
        throw new Error('AI가 음식 이름을 인식하지 못했습니다.');
      }
      
      // ===== 2단계: 인식된 이름으로 DB에서 음식 정보 검색 (food_id 획득) =====
      alert(`'${recognizedFoodName}'(으)로 음식을 검색합니다...`);
      const searchResponse = await apiClient.get(`/v1/food/search?q=${recognizedFoodName}`);
      
      if (searchResponse.data.results.length === 0) {
        throw new Error(`'${recognizedFoodName}'에 해당하는 음식을 DB에서 찾을 수 없습니다.`);
      }

      // 검색 결과의 첫 번째 항목을 사용
      const foodData = searchResponse.data.results[0];
      const foodId = foodData.food_id;

      // ===== 3단계: 획득한 food_id로 최종 식단 기록 =====
      alert(`'${foodData.food_name}'을(를) 식단에 기록합니다.`);
      const userId = localStorage.getItem('user_id');

      const recordPayload = {
        user_id: parseInt(userId, 10),
        food_id: foodId,
        serving_amount: 1.0, // 기본 1인분
      };

      await apiClient.post('/v1/food/record', recordPayload);

      // ===== 4단계: 성공 후 대시보드 새로고침 =====
      alert('성공적으로 기록되었습니다!');
      fetchData();

    } catch (error) {
      console.error('음식 기록 처리 중 오류 발생:', error);
      alert(error.message || '음식 기록 과정에서 오류가 발생했습니다.');
    } finally {
      // 동일한 파일을 다시 선택할 수 있도록 입력 값을 초기화
      event.target.value = null;
    }
  };


  if (loading) return <div className={styles.loadingMessage}>로딩 중...</div>;

  // DashboardPage.jsx 파일의 return 문 바로 위
    const consumedKcal = data ? data.consumed_calories : 0;
    const goalKcal = data ? data.daily_target_calories : 2000;
    const foodLogs = data ? data.meals : [];
    // 프로그레스 바의 진행률을 계산 (0% ~ 100%)
    const progressPercentage = goalKcal > 0 ? Math.min((consumedKcal / goalKcal) * 100, 100) : 0;

    let remainingKcal = goalKcal - consumedKcal;
    if (isNaN(remainingKcal)) {
    remainingKcal = 0;
    }

  return (
    <div className={styles.container}>
      {/* 화면에는 보이지 않는 파일 입력 필드 */}
      <input
        type="file"
        accept="image/*"
        ref={fileInputRef}
        onChange={handleFileChange}
        style={{ display: 'none' }}
      />
      
      {/* 기존 JSX... */}
      <header className={styles.header}>
        <h1>Kcali</h1>
        <p className={styles.slogan}>사진 한 장으로 간편하게 시작하는<br/>나만의 식단 관리</p>
      </header>

      <main className={styles.mainContent}>
        <section className={styles.summary}>
          <span>섭취: {consumedKcal}</span>
          <span className={styles.goal}>/ 목표: {goalKcal} kcal</span>
        </section>

        {/* ===== 👇 여기에 프로그레스 바 섹션을 추가합니다 ===== */}
        <section className={styles.progressContainer}>
          <div className={styles.progressBar}>
            <div 
              className={styles.progress} 
              style={{ width: `${progressPercentage}%` }}
            ></div>
          </div>
        </section>
        {/* ============================================== */}

        <section className={styles.statusMessage}>
          {remainingKcal >= 0 ? (
            <p>“오늘 <span className={styles.highlight}>{remainingKcal}</span> 칼로리 더 드실 수 있어요!”</p>
          ) : (
            <p className={styles.warning}>“오늘 더이상 드시면 안돼요!”</p>
          )}
        </section>

        <section className={styles.logSection}>
        <h2>⬇️ 오늘 먹은 음식</h2>
        <ul className={styles.logList}>
            {foodLogs && foodLogs.length > 0
            ? foodLogs.map((log, index) => (
                // key prop에는 백엔드에서 받은 고유 ID인 'record_id'를 사용합니다.
                // 백엔드 데이터에 맞춰 'food_name'과 'calories'로 속성 이름을 변경합니다.
                <li key={log.record_id || index}>
                    - {log.food_name} ({log.calories} kcal)
                </li>
                ))
            : <li>오늘 먹은 음식이 없습니다.</li>
            }
        </ul>
        </section>
      </main>

      {/* + 버튼에 onClick 핸들러 연결 */}
      <button className={styles.addButton} onClick={handleAddClick}>+</button>
    </div>
  );
}

export default DashboardPage;