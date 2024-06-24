import styled, { keyframes } from "styled-components";
import { summonerId } from "./summoner_item";
import nullImage from "../assets/null.png";
const spin = keyframes`
    0% {
      --rotate: 0deg;
    }
    100% {
      --rotate: 360deg;
    }
`;
export const GameItem = styled.div`
  display: flex;
  @property --rotate {
    syntax: "<angle>";
    initial-value: 132deg;
    inherits: false;
  }

  background-image: ${(props) =>
    props.win === false
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

const ChampImage = styled.img`
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-bottom: 10px;
`;

const DataContainer = styled.div`
  flex: 1;
  display: flex;
  margin 10px;
  padding: 10px;
  padding-left: 30px;
  flex-direction: column;
`;

const ItemContainer = styled.div`
  display: flex;
`;

const TeamIcon = styled.img`
  width: 30px;
  height: 30px;
`;

const LastContainer = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  padding-top: 20px;
`;
const TextWithEllipsis = styled.div`
  width: 70px; // 고정 너비 설정, 필요에 따라 조정 가능
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  margin: 5px;
`;
const GameItems = ({ game, onClick, puuid }) => {
  // const result = useSelector((state) => state.getPuuid.result);
  console.log(game);

  const my_game = game.participants.find(
    (participant) => participant.puuid === puuid
  );
  if (my_game?.win === undefined) {
    return <div></div>;
  }
  const blue_player = game.participants.filter((participant) => {
    return participant.teamId === 100;
  });

  const red_player = game.participants.filter((participant) => {
    return participant.teamId === 200;
  });

  function createItemUrl(item_id) {
    const url = `https://opgg-static.akamaized.net/meta/images/lol/14.12.1/item/${item_id}.png`;
    return url;
  }

  function createPerkUrl(item_id) {
    const url = `https://opgg-static.akamaized.net/meta/images/lol/14.12.1/perk/${item_id}.png`;
    return url;
  }
  function createSummonerUrl(item_id) {
    const url = `https://opgg-static.akamaized.net/meta/images/lol/14.12.1/spell/${item_id}.png`;
    return url;
  }
  function createChampionUrl(item_id) {
    const url = `https://opgg-static.akamaized.net/meta/images/lol/14.12.1/champion/${item_id}.png`;
    return url;
  }

  return (
    <GameItem win={my_game.win} onClick={onClick}>
      <ChampImage src={createChampionUrl(my_game.championName)} />
      <DataContainer>
        {my_game.kills} / {my_game.deaths} / {my_game.assists}
        <ItemContainer>
          <TeamIcon
            src={createSummonerUrl(summonerId[my_game.summoner1Id])}
            onError={(e) => {
              e.target.onerror = null; // 무한 루프 방지
              e.target.src = nullImage; // 에러 시 대체 이미지 설정
            }}
          />
          <TeamIcon
            src={createSummonerUrl(summonerId[my_game.summoner2Id])}
            onError={(e) => {
              e.target.onerror = null; // 무한 루프 방지
              e.target.src = nullImage; // 에러 시 대체 이미지 설정
            }}
          />
          <TeamIcon
            src={createPerkUrl(my_game.perks.styles[0].selections[0].perk)}
            onError={(e) => {
              e.target.onerror = null; // 무한 루프 방지
              e.target.src = nullImage; // 에러 시 대체 이미지 설정
            }}
          />
          <TeamIcon
            src={createPerkUrl(my_game.perks.styles[0].selections[1].perk)}
            onError={(e) => {
              e.target.onerror = null; // 무한 루프 방지
              e.target.src = nullImage; // 에러 시 대체 이미지 설정
            }}
          />
          <TeamIcon
            src={createPerkUrl(my_game.perks.styles[0].selections[2].perk)}
            onError={(e) => {
              e.target.onerror = null; // 무한 루프 방지
              e.target.src = nullImage; // 에러 시 대체 이미지 설정
            }}
          />
          <TeamIcon
            src={createPerkUrl(my_game.perks.styles[0].selections[3].perk)}
            onError={(e) => {
              e.target.onerror = null; // 무한 루프 방지
              e.target.src = nullImage; // 에러 시 대체 이미지 설정
            }}
          />
        </ItemContainer>
        <ItemContainer>
          <TeamIcon
            src={createItemUrl(my_game.item0)}
            onError={(e) => {
              e.target.onerror = null; // 무한 루프 방지
              e.target.src = nullImage; // 에러 시 대체 이미지 설정
            }}
          />
          <TeamIcon
            src={createItemUrl(my_game.item1)}
            onError={(e) => {
              e.target.onerror = null; // 무한 루프 방지
              e.target.src = nullImage; // 에러 시 대체 이미지 설정
            }}
          />
          <TeamIcon
            src={createItemUrl(my_game.item2)}
            onError={(e) => {
              e.target.onerror = null; // 무한 루프 방지
              e.target.src = nullImage; // 에러 시 대체 이미지 설정
            }}
          />
          <TeamIcon
            src={createItemUrl(my_game.item3)}
            onError={(e) => {
              e.target.onerror = null; // 무한 루프 방지
              e.target.src = nullImage; // 에러 시 대체 이미지 설정
            }}
          />
          <TeamIcon
            src={createItemUrl(my_game.item4)}
            onError={(e) => {
              e.target.onerror = null; // 무한 루프 방지
              e.target.src = nullImage; // 에러 시 대체 이미지 설정
            }}
          />
          <TeamIcon
            src={createItemUrl(my_game.item5)}
            onError={(e) => {
              e.target.onerror = null; // 무한 루프 방지
              e.target.src = nullImage; // 에러 시 대체 이미지 설정
            }}
          />
          <TeamIcon
            src={createItemUrl(my_game.item6)}
            onError={(e) => {
              e.target.onerror = null; // 무한 루프 방지
              e.target.src = nullImage; // 에러 시 대체 이미지 설정
            }}
          />
        </ItemContainer>
      </DataContainer>

      <LastContainer>
        <ItemContainer>
          {blue_player.map((player) => (
            <>
              <TeamIcon
                src={createChampionUrl(player.championName)}
                onError={(e) => {
                  e.target.onerror = null; // 무한 루프 방지
                  e.target.src = nullImage; // 에러 시 대체 이미지 설정
                }}
              />
              <TextWithEllipsis>{player.riotIdGameName}</TextWithEllipsis>
            </>
            // Player Name
          ))}
        </ItemContainer>
        <ItemContainer>
          {red_player.map((player) => (
            <>
              <TeamIcon
                src={createChampionUrl(player.championName)}
                onError={(e) => {
                  e.target.onerror = null; // 무한 루프 방지
                  e.target.src = nullImage; // 에러 시 대체 이미지 설정
                }}
              />
              <TextWithEllipsis>{player.riotIdGameName}</TextWithEllipsis>
            </>
          ))}
        </ItemContainer>
      </LastContainer>
    </GameItem>
  );
};
export default GameItems;
