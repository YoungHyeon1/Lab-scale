import React from "react";
import styled, { keyframes } from "styled-components";

// 애니메이션 키프레임 정의
const fadeIn = keyframes`
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
`;

// 스타일 컴포넌트 정의
const NotFoundContainer = styled.div`
  padding: 20px;
  background-color: #2c3e50; // 어두운 배경색, 게임 테마에 맞춤
  color: #ecf0f1; // 밝은 글자색
  text-align: center;
  border-radius: 8px;
  margin: 20px;
  font-size: 1.5em;
  font-family: "Arial", sans-serif;
  animation: ${fadeIn} 1s ease-out;

  @media (max-width: 768px) {
    font-size: 1.2em; // 모바일 기기에 맞는 글자 크기 조정
  }
`;

const NotFound = ({ Text }) => {
  return <NotFoundContainer>{Text}</NotFoundContainer>;
};

export default NotFound;
