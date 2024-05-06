import React from "react";
import { SearchBar } from "./SearchBar";
import { GameStats } from "./GameStats";
import PredictionResult from "./PredictionResult";
import styled from "styled-components";
import { useSelector } from "react-redux";
import SidebarComponent from "./SidebarComponent";

const MainContainer = styled.div`
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  text-align: center;
`;

const MainPage = () => {
  const { stats } = useSelector((state) => state.gameStats);

  return (
    <MainContainer>
      <SidebarComponent />
      <h1>사이트 이름</h1>
      <SearchBar />
      {stats ? (
        <div />
      ) : (
        <>
          <GameStats />
          <PredictionResult />
        </>
      )}
    </MainContainer>
  );
};

export default MainPage;
