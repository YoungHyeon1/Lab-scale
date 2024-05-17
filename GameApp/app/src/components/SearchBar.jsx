import styled from "styled-components";
import { useDispatch } from "react-redux";
import { fetchGameStats } from "../redux/gameStatsSlice";

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
        placeholder="ex) hide on bush"
        onKeyUp={handleKeyPress}
      />
      
      <StyledButton onClick={handleSearch}>Search</StyledButton>
    </div>
  );
};
