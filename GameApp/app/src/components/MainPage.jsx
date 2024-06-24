import React from "react";
import SearchBar from "./SearchBar";
import styled from "styled-components";
import SidebarComponent from "./SidebarComponent";
import recodingOfLolImage from "./assets/Recoding Of LoL 이미지.png";

const MainContainer = styled.div`
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  text-align: center;
`;

const StyledImage = styled.img`
  width: 70%;
  max-width: 300px;
  height: auto;
  display: block;
  margin: 0 auto;
`;

const MainPage = () => {
  return (
    <MainContainer>
      <SidebarComponent />
      <StyledImage src={recodingOfLolImage} alt="Recoding Of LoL" />
      <SearchBar />
    </MainContainer>
  );
};

export default MainPage;
