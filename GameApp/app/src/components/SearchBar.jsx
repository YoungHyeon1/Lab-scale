import styled from "styled-components";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

const SearchContainer = styled.div`
  display: flex;
  align-items: center;
  background-color: white;
  border-radius: 25px;
  padding: 5px 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  height: 50px;
  width: 70%; /* 너비를 80%로 설정 */
  max-width: 600px; /* 최대 너비 설정 */
  margin: 1.5% auto; /* 중앙 정렬 */
`;

const SearchIcon = styled.span`
  font-size: 20px;
  margin-right: 10px;
  color: #555;
`;

const SearchInput = styled.input`
  border: none;
  outline: none;
  font-size: 16px;
  color: #212529;
  flex-grow: 1;
  &::placeholder {
    color: #adb5bd;
  }
`;

const SearchButton = styled.button`
  background-color: #007bff;
  border: none;
  border-radius: 20px;
  width: 60px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  margin-left: 20px;
`;

const SearchBar = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const navigate = useNavigate();

  const handleSearch = () => {
    searchTerm.replace("#", "-");
    const convert_url = searchTerm.replace(/#/g, "-");
    navigate(`/research/${convert_url}`);
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      const convert_url = searchTerm.replace(/#/g, "-");
      navigate(`/research/${convert_url}`);
    }
  };

  const handleChange = (event) => {
    // summonerName.replace("#", "-");
    setSearchTerm(event.target.value);
  };

  return (
    <SearchContainer>
      <SearchIcon>🔍</SearchIcon>
      <SearchInput
        type="text"
        placeholder="플레이어 이름 + #KR1"
        value={searchTerm}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
      />
      <SearchButton onClick={handleSearch}>검색</SearchButton>
    </SearchContainer>
  );
};

export default SearchBar;
