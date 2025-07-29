import React, { useState, useEffect } from 'react';
import apiClient from '../api/client';
import styles from './DashboardPage.module.css';

function DashboardPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await apiClient.get('/v1/dashboard/today/');
        setData(response.data);
      } catch (error) {
        console.error("데이터 로딩 실패", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div className={styles.message}>로딩 중...</div>;
  if (!data) return <div className={styles.message}>데이터를 불러올 수 없습니다.</div>;

  const consumedPercent = (data.consumed_kcal / data.goal_kcal) * 100;

  return (
    <div className={styles.container}>
      <div className={styles.dashboard}>
        <header className={styles.header}>
          <h2>오늘의 식단</h2>
        </header>
        
        <section className={styles.summaryCard}>
          <div className={styles.calorieInfo}>
            <span className={styles.consumed}>{data.consumed_kcal}</span>
            <span className={styles.goal}>/ {data.goal_kcal} kcal</span>
          </div>
          <div className={styles.progressBar}>
            <div className={styles.progress} style={{ width: `${consumedPercent}%` }}></div>
          </div>
        </section>

        <section className={styles.logSection}>
          <h3>오늘 먹은 음식</h3>
          <ul className={styles.logList}>
            {data.food_logs.map(log => (
              <li key={log.id} className={styles.logItem}>
                <span>{log.name}</span>
                <span>{log.kcal} kcal</span>
              </li>
            ))}
          </ul>
        </section>

        <button className={styles.addButton}>+</button>
      </div>
    </div>
  );
}

export default DashboardPage;