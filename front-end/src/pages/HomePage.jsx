import React from 'react';
import { Link } from 'react-router-dom';
import styles from './HomePage.module.css';

function HomePage() {
  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1>Kcali</h1>
      </header>
      <main className={styles.main}>
        <div className={styles.hero}>
          <h2 className={styles.title}>
            사진 한 장으로 간편하게,
            <br />
            나만의 식단 관리 시작하기
          </h2>
          <p className={styles.subtitle}>
            Kcali는 AI를 통해 당신의 식단을 분석하고
            <br />
            건강한 식습관을 만들어나갈 수 있도록 돕습니다.
          </p>
          <div className={styles.buttonGroup}>
            <Link to="/signup" className={styles.primaryButton}>
              지금 시작하기
            </Link>
            <Link to="/login" className={styles.secondaryButton}>
              로그인
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}

export default HomePage;