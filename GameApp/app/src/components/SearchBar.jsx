import styled from "styled-components";
import { useDispatch } from "react-redux";
import { fetchGameStats } from "../redux/gameStatsSlice";

const StyledInput = styled.input`
  padding: 10px;
  margin: 10px;
  width: 300px;
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

  const handleSearch = () => {
    if (input.value) {
      dispatch(fetchGameStats(input.value));
      input.value = "";
    }
  };

  return (
    <div>
      <StyledInput ref={(node) => (input = node)} placeholder="Summoner Name" />
      <StyledButton onClick={handleSearch}>Search</StyledButton>
    </div>
  );
};
