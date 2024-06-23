import React, { useState } from 'react';
import styled from 'styled-components';

const SearchContainer = styled.div`
  display: flex;
  align-items: center;
  background-color: #f0f0f0; // 배경색 (원하는 색상으로 변경)
  padding: 8px;
  border-radius: 4px;
  width: 20%; // 원하는 너비 (%)
`;

const SearchInput = styled.input`
  flex-grow: 1;
  padding: 8px;
  border: none;
  outline: none;
  border-radius: 4px 0 0 4px; // 왼쪽 모서리 둥글게
`;

const SearchButton = styled.button`
  padding: 8px 12px;
  background-color: #007bff; // 버튼 색상 (원하는 색상으로 변경)
  color: white;
  border: none;
  border-radius: 0 4px 4px 0; // 오른쪽 모서리 둥글게
  cursor: pointer;

  &:hover {
    background-color: #0056b3; // 호버 시 색상 변경
  }
`;

function PredictSC() {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearch = () => {
    // 검색 로직 구현 (API 호출 등)
    console.log('검색어:', searchTerm);
  };

  return (
    <SearchContainer>
      <SearchInput
        type="text"
        placeholder="플레이어 이름 + KR1"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <SearchButton onClick={handleSearch}>검색</SearchButton>
    </SearchContainer>
  );
}

export default PredictSC;

