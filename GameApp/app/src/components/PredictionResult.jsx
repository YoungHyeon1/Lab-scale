import styled from "styled-components";
import { useSelector } from "react-redux";

const PredictionContainer = styled.div`
  padding: 20px;
  margin-top: 20px;
  background-color: #f4f4f8;
  border-radius: 8px;
`;

const PredictionResult = () => {
  const { stats } = useSelector((state) => state.gameStats);

  return (
    <PredictionContainer>
      <h3>Win Rate Prediction</h3>
      {stats.winRate ? (
        <p>Predicted win rate: {stats.winRate}%</p>
      ) : (
        <p>Win rate prediction not available.</p>
      )}
    </PredictionContainer>
  );
};

export default PredictionResult;
