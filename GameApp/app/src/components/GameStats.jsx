import { useSelector } from "react-redux";
import styled from "styled-components";

const StatsContainer = styled.div`
  padding: 20px;
  margin-top: 20px;
  border: 1px solid #ddd;
`;

export const GameStats = () => {
  const { stats, loading, error } = useSelector((state) => state.gameStats);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <StatsContainer>
      {Object.keys(stats).length ? (
        <div>
          <h2>Summoner: {stats.name}</h2>
          <p>Level: {stats.summonerLevel}</p>
          {/* More stats can be displayed here */}
        </div>
      ) : (
        <p>No data found.</p>
      )}
    </StatsContainer>
  );
};
