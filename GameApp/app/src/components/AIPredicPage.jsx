import SearchBar from "./SearchBar";
import SidebarComponent from "./SidebarComponent";
import styled from "styled-components";

const PromoContainer = styled.div`
  padding: 20px;
  margin: 20px auto;
  max-width: 800px;
  background-color: #f4f4f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  font-family: "Helvetica", "Arial", sans-serif;
`;

const PromoText = styled.p`
  color: #555;
  font-size: 18px;
`;

const Table = styled.table`
  width: 80%;
  margin: 20px auto;
  border-collapse: collapse;
`;

const Th = styled.th`
  background-color: #333;
  color: white;
  padding: 10px 15px;
`;

const Td = styled.td`
  text-align: center;
  padding: 8px 12px;
  background-color: #f9f9f9;
  border-bottom: 1px solid #ddd;
`;

const StatHeader = styled.h2`
  text-align: center;
  color: #333;
`;

const AIPredicPage = () => {
  const stats = [
    {
      tier: "Diamond",
      champion: "Ahri",
      gamesPlayed: 40,
      wins: 30,
      losses: 10,
    },
    {
      tier: "Platinum",
      champion: "Lee Sin",
      gamesPlayed: 50,
      wins: 28,
      losses: 22,
    },
    { tier: "Gold", champion: "Yasuo", gamesPlayed: 60, wins: 30, losses: 30 },
    { tier: "Silver", champion: "Zed", gamesPlayed: 70, wins: 35, losses: 35 },
    { tier: "Bronze", champion: "Teemo", gamesPlayed: 20, wins: 5, losses: 15 },
    {
      tier: "Diamond",
      champion: "Kai'Sa",
      gamesPlayed: 45,
      wins: 30,
      losses: 15,
    },
    { tier: "Gold", champion: "Thresh", gamesPlayed: 40, wins: 22, losses: 18 },
    { tier: "Silver", champion: "Jhin", gamesPlayed: 30, wins: 17, losses: 13 },
    {
      tier: "Platinum",
      champion: "Ezreal",
      gamesPlayed: 55,
      wins: 32,
      losses: 23,
    },
    {
      tier: "Diamond",
      champion: "Soraka",
      gamesPlayed: 25,
      wins: 20,
      losses: 5,
    },
    { tier: "Bronze", champion: "Nasus", gamesPlayed: 15, wins: 2, losses: 13 },
    { tier: "Gold", champion: "Nami", gamesPlayed: 50, wins: 27, losses: 23 },
    {
      tier: "Silver",
      champion: "Garen",
      gamesPlayed: 40,
      wins: 18,
      losses: 22,
    },
  ];

  return (
    <>
      <SidebarComponent />
      <SearchBar />
      <PromoContainer>
        <PromoText>
          전투를 시작하기 전에 승리를 예측하세요!
          <br /> 우리의 AI 기반 승률 예측 서비스로 당신의 다음 게임의 우위를
          확보하세요.
        </PromoText>
      </PromoContainer>
      <StatHeader>게임 통계</StatHeader>
      <Table>
        <thead>
          <tr>
            <Th>티어</Th>
            <Th>챔피언</Th>
            <Th>경기 수</Th>
            <Th>승리</Th>
            <Th>패배</Th>
          </tr>
        </thead>
        <tbody>
          {stats.map((stat, index) => (
            <tr key={index}>
              <Td>{stat.tier}</Td>
              <Td>{stat.champion}</Td>
              <Td>{stat.gamesPlayed}</Td>
              <Td>{stat.wins}</Td>
              <Td>{stat.losses}</Td>
            </tr>
          ))}
        </tbody>
      </Table>
    </>
  );
};

export default AIPredicPage;
