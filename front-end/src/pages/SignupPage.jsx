import React, { useState } from 'react';
import apiClient from '../api/client';
import styles from './SignupPage.module.css'; // CSS 모듈 import
import { Link, useNavigate } from 'react-router-dom'; // Link 추가

function SignupPage() {
  const navigate = useNavigate(); // ✅ 선언 추가
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    password_check: '',
    gender: 'male',
    age: '',
    height: '',
    weight: '',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.password_check) {
      alert('비밀번호가 일치하지 않습니다.');
      return;
    }
    try {
      const response = await apiClient.post('/v1/users/signup/', formData);
      alert(response.data.message);
      // 성공 시 로그인 페이지로 이동
      navigate('/login'); // ✅ 회원가입 성공 시 로그인 페이지로 이동
    } catch (error) {
      alert('회원가입에 실패했습니다. 입력 정보를 확인해주세요.');
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
          <input type="password" name="password_check" placeholder="password check" value={formData.password_check} onChange={handleChange} required />
          <input type="text" name="gender" placeholder="gender (male/female)" value={formData.gender} onChange={handleChange} />
          <input type="number" name="age" placeholder="age" value={formData.age} onChange={handleChange} />
          <input type="number" name="height" placeholder="height (cm)" value={formData.height} onChange={handleChange} />
          <input type="number" name="weight" placeholder="weight (kg)" value={formData.weight} onChange={handleChange} />
        </div>
        
        <button type="submit" className={styles.button}>Sign Up</button>
      </form>
    </div>
  );
}

export default SignupPage;