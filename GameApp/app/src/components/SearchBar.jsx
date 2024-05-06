import styled from "styled-components";
import { useDispatch } from "react-redux";
import { fetchGameStats } from "../redux/gameStatsSlice";

const StyledInput = styled.input`
  padding: 10px;
  margin: 5px;
  width: 300px;
`;
const TagInput = styled.input`
  padding: 10px;
  margin: 5px;
  width: 100px;
`;

const StyledButton = styled.button`
  padding: 10px 20px;
  background-color: blue;
  color: white;
  border: none;
  cursor: pointer;
`;

export const SearchBar = () => {
  const dispatch = useDispatch();
  let input;
  let tag;

  const handleSearch = () => {
    if (input.value) {
      let summonerName = input.value + "#" + tag.value;
      dispatch(fetchGameStats(summonerName));
      input.value = "";
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
        placeholder="소환사 이름"
        onKeyUp={handleKeyPress}
      />
      <TagInput
        ref={(node) => (tag = node)}
        placeholder="테그라인"
        onKeyUp={handleKeyPress}
      />
      <StyledButton onClick={handleSearch}>검색</StyledButton>
    </div>
  );
};
