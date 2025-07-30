import React, { useState, useEffect } from 'react';
import apiClient from '../api/client';
import styles from './DashboardPage.module.css';

function DashboardPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  // 목업과 같은 디자인을 보기 위한 임시 데이터
  // 실제 API 연동 시에는 이 부분을 삭제하세요.
  const mockData = {
    consumed_kcal: 360,
    goal_kcal: 2000,
    food_logs: [
      { id: 1, name: '계란 후라이', kcal: 180 },
      { id: 2, name: '닭가슴살 샐러드', kcal: 180 },
    ],
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        // 실제 API를 사용할 때는 아래 주석을 해제하세요.
        const response = await apiClient.get('/v1/dashboard/today/');
        setData(response.data);
        
        // 임시 목업 데이터 사용
        //setData(mockData);

      } catch (error) {
        console.error("데이터 로딩 실패", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div className={styles.loadingMessage}>로딩 중...</div>;
  
  // 데이터가 없을 때의 기본값 설정
  const consumedKcal = data ? data.consumed_kcal : 0;
  const goalKcal = data ? data.goal_kcal : 2000;
  const foodLogs = data ? data.food_logs : [];
  const remainingKcal = goalKcal - consumedKcal;

  return (
    <div className={styles.container}>
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
            {foodLogs.length > 0 ? (
              foodLogs.map(log => (
                <li key={log.id}>- {log.name} ({log.kcal} kcal)</li>
              ))
            ) : (
              <li>오늘 먹은 음식이 없습니다.</li>
            )}
          </ul>
        </section>
      </main>

      <button className={styles.addButton}>+</button>
    </div>
  );
}

export default DashboardPage;