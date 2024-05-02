import React from "react";
import { SearchBar } from "./SearchBar";
import { GameStats } from "./GameStats";
import PredictionResult from "./PredictionResult";
import styled from "styled-components";

const MainContainer = styled.div`
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
`;

const MainPage = () => {
  return (
    <MainContainer>
      <h1>Game Stats Tracker</h1>
      <SearchBar />
      <GameStats />
      <PredictionResult />
    </MainContainer>
  );
};

export default MainPage;
