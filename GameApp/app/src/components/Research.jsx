import SidebarComponent from "./SidebarComponent";
import React, { useEffect } from "react";
import SearchBar from "./SearchBar";
import ProfileCard from "./module/ProfileCard";
import GameList from "./module/GameList";
import { useParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { fetchPuuid } from "../redux/getPuuidSlice";
import { fetchUserLeague } from "../redux/userLeagueSlice";
import { fetchMatches } from "../redux/matchSlice";
import { useState } from "react";
import NotFound from "./module/NotFound";

function Research() {
  const { gameName } = useParams();
  const dispatch = useDispatch();
  const { result, userLeague, matches } = useSelector((state) => ({
    result: state.getPuuid.result,
    userLeague: state.userLeague.userLeague,
    matches: state.match.matches,
  }));

  const [index, setIndex] = useState(1);

  useEffect(() => {
    dispatch(fetchPuuid(gameName));
  }, [dispatch, gameName]);

  useEffect(() => {
    if (result) {
      dispatch(fetchUserLeague(result.puuid));
    }
  }, [dispatch, result]);

  useEffect(() => {
    if (result) {
      dispatch(fetchMatches({ puuid: result.puuid, index }));
    }
  }, [dispatch, result, index]);

  return (
    <>
      <SidebarComponent />
      <SearchBar />
      {result && userLeague ? (
        <>
          <ProfileCard
            profile={{
              imageUrl: `https://opgg-static.akamaized.net/meta/images/profile_icons/profileIcon${result.profile_icon_id}.jpg`,
              level: result.summoner_level,
              lastUpdated: result.revision_date,
              name: result.game_name,
              tag: result.tag_line,
              leagues: userLeague.map(
                ({
                  name,
                  tier,
                  rank,
                  leaguePoints,
                  wins,
                  losses,
                  queue_type,
                }) => ({
                  leagueName: name,
                  rankIconUrl: `https://opgg-static.akamaized.net/images/medals_new/${tier.toLowerCase()}.png`,
                  tier,
                  rank,
                  wins,
                  losses,
                  queue_type,
                  winRate: Math.round((wins / (wins + losses)) * 100),
                  points: leaguePoints,
                })
              ),
            }}
          />
        </>
      ) : (
        <NotFound Text={"이런! 찾으시는 프로필이 존재하지 않습니다."} />
      )}
      {matches ? (
        <GameList games={matches} puuid={result.puuid} />
      ) : (
        <NotFound Text={`찾으시는 매치 정보를 찾을 수 없습니다.`} />
      )}
    </>
  );
}

export default Research;
