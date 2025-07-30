import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom'; // Link 추가
import apiClient from '../api/client';
import styles from './SignupPage.module.css'; // 회원가입 CSS 재사용

function LoginPage() {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await apiClient.post('/v1/users/login/', formData);
      // 'user_id' 대신 'access_token'을 저장합니다. (원래 방식)
      localStorage.setItem('accessToken', response.data.access_token);
      alert('로그인 성공!');
      navigate('/dashboard');
    } catch (error) {
      alert('로그인에 실패했습니다. 이메일과 비밀번호를 확인해주세요.');
      console.error(error);
    }
  };

  return (
    <div className={styles.container}>
      <form className={styles.form} onSubmit={handleSubmit}>
        <h1 className={styles.title}>Kcali</h1>
        <p className={styles.subtitle}>사진 한 장으로 간편하게 시작하는<br/>나만의 식단 관리</p>

        <div className={styles.inputGroup}>
          <input type="email" name="email" placeholder="email" value={formData.email} onChange={handleChange} required />
          <input type="password" name="password" placeholder="password" value={formData.password} onChange={handleChange} required />
        </div>
        
        {/* ===== 수정된 부분 ===== */}
        <div className={styles.buttonGroup}>
          <button type="submit" className={styles.button}>Sign In</button>
          <Link to="/signup" className={styles.secondaryButton}>Sign Up</Link>
        </div>
        {/* ===================== */}
      </form>
    </div>
  );
}

export default LoginPage;