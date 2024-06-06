import styled from "styled-components";
import { useDispatch } from "react-redux";
import { fetchGameStats } from "../redux/gameStatsSlice";
import { useNavigate } from "react-router-dom";

const StyledInput = styled.input`
  padding: 10px;
  width: 300px;

`;
const StyledButton = styled.button`
padding: 12px 20px;
background-color: blue;
color: white;
border: none;
cursor: pointer;
`;


export const SearchBar = ({onError}) => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  let input;
  let tag;

  const handleSearch = () => {
    
    if (input.value) {
      let summonerName = input.value + "#" + tag.value;
      dispatch(fetchGameStats(summonerName));
      input.value = "";
    }else{
      try {
        navigate('/about');
        // 검색 로직 예시
        throw new Error('검색 오류가 발생했습니다.');
      } catch (error) {
        onError(error.message);
      }
    }
  };
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div>
      <StyledInput
        ref={(node) => (input = node)}
        placeholder="ex) hide on bush"
        onKeyUp={handleKeyPress}
      />
      
      <StyledButton onClick={handleSearch}>Search</StyledButton>
    </div>
  );
  
};
