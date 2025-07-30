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
      console.log(userId);
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

  // 파일이 선택되었을 때 실행될 핸들러
  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) {
      return; // 파일이 선택되지 않았으면 아무것도 안 함
    }

    // FormData 객체를 사용하여 파일을 담음
    const formData = new FormData();
    // 백엔드에서 받을 key 이름을 'image'로 가정합니다.
    formData.append('file', file);

    try {
      alert('이미지를 업로드합니다...');
      await apiClient.post('/v1/food/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      alert('업로드 성공! 데이터를 새로고침합니다.');
      fetchData(); // 업로드 성공 시 대시보드 데이터를 다시 불러옴

    } catch (error) {
      console.error('이미지 업로드 실패:', error);
      alert('이미지 업로드에 실패했습니다.');
    } finally {
        // 동일한 파일을 다시 선택할 수 있도록 입력 값을 초기화
        event.target.value = null;
    }
  };


  if (loading) return <div className={styles.loadingMessage}>로딩 중...</div>;

  const consumedKcal = data ? data.consumed_kcal : 0;
  const goalKcal = data ? data.goal_kcal : 2000;
  const foodLogs = data ? data.meals : [];
  const remainingKcal = goalKcal - consumedKcal;

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
            {foodLogs.length > 0 
            ? foodLogs.map(log => (
                <li key={log.id}>- {log.name} ({log.kcal} kcal)</li>
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