import React, { useState } from "react";
import styled, { keyframes } from "styled-components";
import GameModal from "./GameModal";
/*
const spin = keyframes`
    0% {
      --rotate: 0deg;
    }
    100% {
      --rotate: 360deg;
    }
`;

export const GameListContainer = styled.div`
  margin: 20px;
  display: flex;
  flex-direction: column;
`;

export const GameItem = styled.div`
  @property --rotate {
    syntax: "<angle>";
    initial-value: 132deg;
    inherits: false;
  }

  background-image: ${(props) =>
    props.team === "Red"
      ? "linear-gradient(var(--rotate),#ffc4ec -10%,#efdbfd 50%,#ffedd6 110%)"
      : "linear-gradient(var(--rotate),#c9f7f5 -10%,#a0e9e6 50%,#86cfcb 110%)"};
  animation: ${spin} 3.5s linear infinite;

  padding: 0.8em 1.4em;
  position: relative;
  isolation: isolate;
  border-radius: 0.66em;
  transition: all var(--spring-duration) var(--spring-easing);
  margin: 10px 0;
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
          <GameItem
            key={game.id}
            onClick={() => handleShow(game)}
            team={game.team}
          >
            <h3>
              {game.champion} ({game.team} Team)
            </h3>
            <p>
              {game.result} - {game.kills}/{game.deaths}/{game.assists}
            </p>
            <p>{game.date}</p>
          </GameItem>
        ))}

        {selectedGame && (
          <GameModal show={show} onClose={handleClose}>
            <h2>Game Details</h2>
            <p>Champion: {selectedGame.champion}</p>
            <p>Result: {selectedGame.result}</p>
            <p>Team: {selectedGame.team}</p>
            <p>Kills: {selectedGame.kills}</p>
            <p>Deaths: {selectedGame.deaths}</p>
            <p>Assists: {selectedGame.assists}</p>
            <p>Date: {selectedGame.date}</p>
            <CloseButton onClick={handleClose}>Close</CloseButton>
          </GameModal>
        )}
      </GameListContainer>
    </>
  );
};*/


const MatchDetailModal = styled(GameModal)`
  /* GameModal 스타일을 기반으로 필요한 추가 스타일 적용 */
  width: 800px; /* 모달 창 크기 조정 */
`;
export default GameList;
