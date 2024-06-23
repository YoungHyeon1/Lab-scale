import React, { useState } from "react";
import styled from "styled-components";
import GameModal from "./GameModal";
import GameItems from "./GameItems";

export const GameListContainer = styled.div`
  margin: 20px;
  display: flex;
  flex-direction: column;
`;

const CloseButton = styled.button`
  top: 10px;
  right: 10px;
  border: none;
  background: none;
  font-size: 24px;
  cursor: pointer;
`;

const GameList = ({ games }) => {
  const [show, setShow] = useState(false);
  const [selectedGame, setSelectedGame] = useState(null);
  const handleClose = () => setShow(false);
  const handleShow = (game) => {
    setSelectedGame(game);
    setShow(true);
  };

  return (
    <>
      <GameListContainer>
        {games.map((game) => (
          <GameItems game={game} onClick={() => handleShow(game)} />
        ))}

        {selectedGame && (
          <GameModal show={show} onClose={handleClose}>
            <h2>Game Details</h2>
            <p>GameTime: {selectedGame.create_timestamp}</p>
            <p>GameType: {selectedGame.game_type}</p>
            <p>GameMode: {selectedGame.game_mode}</p>
            <CloseButton onClick={handleClose}>Close</CloseButton>
          </GameModal>
        )}
      </GameListContainer>
    </>
  );
};

export default GameList;
