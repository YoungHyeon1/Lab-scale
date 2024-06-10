import React, { useState } from "react";
import SearchBar from "./SearchBar";
import { GameStats } from "./GameStats";
import PredictionResult from "./PredictionResult";
import styled from "styled-components";
import { useSelector } from "react-redux";
import SidebarComponent from "./SidebarComponent";
import { Button, Modal } from "react-bootstrap";
import recodingOfLolImage from "./assets/Recoding Of LoL 이미지.png";

const StyledModal = styled(Modal)`
  .modal-dialog {
    max-width: 600px;
  }

  .modal-content {
    border-radius: 10px;
    background-color: #f8f9fa;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
    border: none;
  }

  .modal-header {
    background-color: #007bff;
    color: white;
    border-bottom: none;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
  }

  .modal-title {
    font-weight: bold;
  }

  .modal-body {
    padding: 20px;
    font-size: 16px;
    color: #343a40;
  }

  .modal-footer {
    border-top: none;
    justify-content: center;
  }

  .btn-secondary {
    background-color: #6c757d;
    border-color: #6c757d;
  }

  .btn-secondary:hover {
    background-color: #5a6268;
    border-color: #545b62;
  }
`;

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
  const [showModal, setShowModal] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const { stats } = useSelector((state) => state.gameStats);
  const handleSearchError = (message) => {
    setErrorMessage(message);
    setShowModal(true);
  };

  const handleClose = () => setShowModal(false);

  return (
    <MainContainer>
      <SidebarComponent />
      <StyledImage src={recodingOfLolImage} alt="Recoding Of LoL" />
      <SearchBar />
      {stats ? (
        <div />
      ) : (
        <>
          <GameStats />
          <PredictionResult />
        </>
      )}
      <StyledModal show={showModal} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>검색 오류 발생</Modal.Title>
        </Modal.Header>
        <Modal.Body>{errorMessage}</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            닫기
          </Button>
        </Modal.Footer>
      </StyledModal>
    </MainContainer>
  );
};

export default MainPage;
